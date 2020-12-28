#include "inner.h"

/*
 * Falcon signature generation.
 *
 * ==========================(LICENSE BEGIN)============================
 *
 * Copyright (c) 2017-2019  Falcon Project
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * ===========================(LICENSE END)=============================
 *
 * @author   Thomas Pornin <thomas.pornin@nccgroup.com>
 */


/* =================================================================== */

/*
 * Compute degree N from logarithm 'logn'.
 */
#define MKN(logn)   ((size_t)1 << (logn))

/* =================================================================== */
/*
 * Binary case:
 *   N = 2^logn
 *   phi = X^N+1
 */

/*
 * Get the size of the LDL tree for an input with polynomials of size
 * 2^logn. The size is expressed in the number of elements.
 */
static inline unsigned
ffLDL_treesize(unsigned logn) {
    /*
     * For logn = 0 (polynomials are constant), the "tree" is a
     * single element. Otherwise, the tree node has size 2^logn, and
     * has two child trees for size logn-1 each. Thus, treesize s()
     * must fulfill these two relations:
     *
     *   s(0) = 1
     *   s(logn) = (2^logn) + 2*s(logn-1)
     */
    return (logn + 1) << logn;
}

/*
 * Inner function for ffLDL_fft(). It expects the matrix to be both
 * auto-adjoint and quasicyclic; also, it uses the source operands
 * as modifiable temporaries.
 *
 * tmp[] must have room for at least one polynomial.
 */
static void
ffLDL_fft_inner(fpr *tree,
                fpr *g0, fpr *g1, unsigned logn, fpr *tmp) {
    size_t n, hn;

    n = MKN(logn);
    if (n == 1) {
        tree[0] = g0[0];
        return;
    }
    hn = n >> 1;

    /*
     * The LDL decomposition yields L (which is written in the tree)
     * and the diagonal of D. Since d00 = g0, we just write d11
     * into tmp.
     */
    PQCLEAN_FALCON512_AVX2_poly_LDLmv_fft(tmp, tree, g0, g1, g0, logn);

    /*
     * Split d00 (currently in g0) and d11 (currently in tmp). We
     * reuse g0 and g1 as temporary storage spaces:
     *   d00 splits into g1, g1+hn
     *   d11 splits into g0, g0+hn
     */
    PQCLEAN_FALCON512_AVX2_poly_split_fft(g1, g1 + hn, g0, logn);
    PQCLEAN_FALCON512_AVX2_poly_split_fft(g0, g0 + hn, tmp, logn);

    /*
     * Each split result is the first row of a new auto-adjoint
     * quasicyclic matrix for the next recursive step.
     */
    ffLDL_fft_inner(tree + n,
                    g1, g1 + hn, logn - 1, tmp);
    ffLDL_fft_inner(tree + n + ffLDL_treesize(logn - 1),
                    g0, g0 + hn, logn - 1, tmp);
}

/*
 * Compute the ffLDL tree of an auto-adjoint matrix G. The matrix
 * is provided as three polynomials (FFT representation).
 *
 * The "tree" array is filled with the computed tree, of size
 * (logn+1)*(2^logn) elements (see ffLDL_treesize()).
 *
 * Input arrays MUST NOT overlap, except possibly the three unmodified
 * arrays g00, g01 and g11. tmp[] should have room for at least three
 * polynomials of 2^logn elements each.
 */
static void
ffLDL_fft(fpr *tree, const fpr *g00,
          const fpr *g01, const fpr *g11,
          unsigned logn, fpr *tmp) {
    size_t n, hn;
    fpr *d00, *d11;

    n = MKN(logn);
    if (n == 1) {
        tree[0] = g00[0];
        return;
    }
    hn = n >> 1;
    d00 = tmp;
    d11 = tmp + n;
    tmp += n << 1;

    memcpy(d00, g00, n * sizeof * g00);
    PQCLEAN_FALCON512_AVX2_poly_LDLmv_fft(d11, tree, g00, g01, g11, logn);

    PQCLEAN_FALCON512_AVX2_poly_split_fft(tmp, tmp + hn, d00, logn);
    PQCLEAN_FALCON512_AVX2_poly_split_fft(d00, d00 + hn, d11, logn);
    memcpy(d11, tmp, n * sizeof * tmp);
    ffLDL_fft_inner(tree + n,
                    d11, d11 + hn, logn - 1, tmp);
    ffLDL_fft_inner(tree + n + ffLDL_treesize(logn - 1),
                    d00, d00 + hn, logn - 1, tmp);
}

/*
 * Normalize an ffLDL tree: each leaf of value x is replaced with
 * sigma / sqrt(x).
 */
static void
ffLDL_binary_normalize(fpr *tree, unsigned logn) {
    /*
     * TODO: make an iterative version.
     */
    size_t n;

    n = MKN(logn);
    if (n == 1) {
        /*
         * We actually store in the tree leaf the inverse of
         * the value mandated by the specification: this
         * saves a division both here and in the sampler.
         */
        tree[0] = fpr_mul(fpr_sqrt(tree[0]), fpr_inv_sigma);
    } else {
        ffLDL_binary_normalize(tree + n, logn - 1);
        ffLDL_binary_normalize(tree + n + ffLDL_treesize(logn - 1),
                               logn - 1);
    }
}

/* =================================================================== */

/*
 * Convert an integer polynomial (with small values) into the
 * representation with complex numbers.
 */
static void
smallints_to_fpr(fpr *r, const int8_t *t, unsigned logn) {
    size_t n, u;

    n = MKN(logn);
    for (u = 0; u < n; u ++) {
        r[u] = fpr_of(t[u]);
    }
}

/*
 * The expanded private key contains:
 *  - The B0 matrix (four elements)
 *  - The ffLDL tree
 */

static inline size_t
skoff_b00(unsigned logn) {
    (void)logn;
    return 0;
}

static inline size_t
skoff_b01(unsigned logn) {
    return MKN(logn);
}

static inline size_t
skoff_b10(unsigned logn) {
    return 2 * MKN(logn);
}

static inline size_t
skoff_b11(unsigned logn) {
    return 3 * MKN(logn);
}

static inline size_t
skoff_tree(unsigned logn) {
    return 4 * MKN(logn);
}

/* see inner.h */
void
PQCLEAN_FALCON512_AVX2_expand_privkey(fpr *expanded_key,
                                      const int8_t *f, const int8_t *g,
                                      const int8_t *F, const int8_t *G,
                                      unsigned logn, uint8_t *tmp) {
    size_t n;
    fpr *rf, *rg, *rF, *rG;
    fpr *b00, *b01, *b10, *b11;
    fpr *g00, *g01, *g11, *gxx;
    fpr *tree;

    n = MKN(logn);
    b00 = expanded_key + skoff_b00(logn);
    b01 = expanded_key + skoff_b01(logn);
    b10 = expanded_key + skoff_b10(logn);
    b11 = expanded_key + skoff_b11(logn);
    tree = expanded_key + skoff_tree(logn);

    /*
     * We load the private key elements directly into the B0 matrix,
     * since B0 = [[g, -f], [G, -F]].
     */
    rf = b01;
    rg = b00;
    rF = b11;
    rG = b10;

    smallints_to_fpr(rf, f, logn);
    smallints_to_fpr(rg, g, logn);
    smallints_to_fpr(rF, F, logn);
    smallints_to_fpr(rG, G, logn);

    /*
     * Compute the FFT for the key elements, and negate f and F.
     */
    PQCLEAN_FALCON512_AVX2_FFT(rf, logn);
    PQCLEAN_FALCON512_AVX2_FFT(rg, logn);
    PQCLEAN_FALCON512_AVX2_FFT(rF, logn);
    PQCLEAN_FALCON512_AVX2_FFT(rG, logn);
    PQCLEAN_FALCON512_AVX2_poly_neg(rf, logn);
    PQCLEAN_FALCON512_AVX2_poly_neg(rF, logn);

    /*
     * The Gram matrix is G = B·B*. Formulas are:
     *   g00 = b00*adj(b00) + b01*adj(b01)
     *   g01 = b00*adj(b10) + b01*adj(b11)
     *   g10 = b10*adj(b00) + b11*adj(b01)
     *   g11 = b10*adj(b10) + b11*adj(b11)
     *
     * For historical reasons, this implementation uses
     * g00, g01 and g11 (upper triangle).
     */
    g00 = (fpr *)tmp;
    g01 = g00 + n;
    g11 = g01 + n;
    gxx = g11 + n;

    memcpy(g00, b00, n * sizeof * b00);
    PQCLEAN_FALCON512_AVX2_poly_mulselfadj_fft(g00, logn);
    memcpy(gxx, b01, n * sizeof * b01);
    PQCLEAN_FALCON512_AVX2_poly_mulselfadj_fft(gxx, logn);
    PQCLEAN_FALCON512_AVX2_poly_add(g00, gxx, logn);

    memcpy(g01, b00, n * sizeof * b00);
    PQCLEAN_FALCON512_AVX2_poly_muladj_fft(g01, b10, logn);
    memcpy(gxx, b01, n * sizeof * b01);
    PQCLEAN_FALCON512_AVX2_poly_muladj_fft(gxx, b11, logn);
    PQCLEAN_FALCON512_AVX2_poly_add(g01, gxx, logn);

    memcpy(g11, b10, n * sizeof * b10);
    PQCLEAN_FALCON512_AVX2_poly_mulselfadj_fft(g11, logn);
    memcpy(gxx, b11, n * sizeof * b11);
    PQCLEAN_FALCON512_AVX2_poly_mulselfadj_fft(gxx, logn);
    PQCLEAN_FALCON512_AVX2_poly_add(g11, gxx, logn);

    /*
     * Compute the Falcon tree.
     */
    ffLDL_fft(tree, g00, g01, g11, logn, gxx);

    /*
     * Normalize tree.
     */
    ffLDL_binary_normalize(tree, logn);
}

typedef int (*samplerZ)(void *ctx, fpr mu, fpr sigma);

/*
 * Perform Fast Fourier Sampling for target vector t. The Gram matrix
 * is provided (G = [[g00, g01], [adj(g01), g11]]). The sampled vector
 * is written over (t0,t1). The Gram matrix is modified as well. The
 * tmp[] buffer must have room for four polynomials.
 */
static void
ffSampling_fft_dyntree(samplerZ samp, void *samp_ctx,
                       fpr *t0, fpr *t1,
                       fpr *g00, fpr *g01, fpr *g11,
                       unsigned logn, fpr *tmp) {
    size_t n, hn;
    fpr *z0, *z1;

    /*
     * Deepest level: the LDL tree leaf value is just g00 (the
     * array has length only 1 at this point); we normalize it
     * with regards to sigma, then use it for sampling.
     */
    if (logn == 0) {
        fpr leaf;

        leaf = g00[0];
        leaf = fpr_mul(fpr_sqrt(leaf), fpr_inv_sigma);
        t0[0] = fpr_of(samp(samp_ctx, t0[0], leaf));
        t1[0] = fpr_of(samp(samp_ctx, t1[0], leaf));
        return;
    }

    n = (size_t)1 << logn;
    hn = n >> 1;

    /*
     * Decompose G into LDL. We only need d00 (identical to g00),
     * d11, and l10; we do that in place.
     */
    PQCLEAN_FALCON512_AVX2_poly_LDL_fft(g00, g01, g11, logn);

    /*
     * Split d00 and d11 and expand them into half-size quasi-cyclic
     * Gram matrices. We also save l10 in tmp[].
     */
    PQCLEAN_FALCON512_AVX2_poly_split_fft(tmp, tmp + hn, g00, logn);
    memcpy(g00, tmp, n * sizeof * tmp);
    PQCLEAN_FALCON512_AVX2_poly_split_fft(tmp, tmp + hn, g11, logn);
    memcpy(g11, tmp, n * sizeof * tmp);
    memcpy(tmp, g01, n * sizeof * g01);
    memcpy(g01, g00, hn * sizeof * g00);
    memcpy(g01 + hn, g11, hn * sizeof * g00);

    /*
     * The half-size Gram matrices for the recursive LDL tree
     * building are now:
     *   - left sub-tree: g00, g00+hn, g01
     *   - right sub-tree: g11, g11+hn, g01+hn
     * l10 is in tmp[].
     */

    /*
     * We split t1 and use the first recursive call on the two
     * halves, using the right sub-tree. The result is merged
     * back into tmp + 2*n.
     */
    z1 = tmp + n;
    PQCLEAN_FALCON512_AVX2_poly_split_fft(z1, z1 + hn, t1, logn);
    ffSampling_fft_dyntree(samp, samp_ctx, z1, z1 + hn,
                           g11, g11 + hn, g01 + hn, logn - 1, z1 + n);
    PQCLEAN_FALCON512_AVX2_poly_merge_fft(tmp + (n << 1), z1, z1 + hn, logn);

    /*
     * Compute tb0 = t0 + (t1 - z1) * l10.
     * At that point, l10 is in tmp, t1 is unmodified, and z1 is
     * in tmp + (n << 1). The buffer in z1 is free.
     *
     * In the end, z1 is written over t1, and tb0 is in t0.
     */
    memcpy(z1, t1, n * sizeof * t1);
    PQCLEAN_FALCON512_AVX2_poly_sub(z1, tmp + (n << 1), logn);
    memcpy(t1, tmp + (n << 1), n * sizeof * tmp);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(tmp, z1, logn);
    PQCLEAN_FALCON512_AVX2_poly_add(t0, tmp, logn);

    /*
     * Second recursive invocation, on the split tb0 (currently in t0)
     * and the left sub-tree.
     */
    z0 = tmp;
    PQCLEAN_FALCON512_AVX2_poly_split_fft(z0, z0 + hn, t0, logn);
    ffSampling_fft_dyntree(samp, samp_ctx, z0, z0 + hn,
                           g00, g00 + hn, g01, logn - 1, z0 + n);
    PQCLEAN_FALCON512_AVX2_poly_merge_fft(t0, z0, z0 + hn, logn);
}

/*
 * Perform Fast Fourier Sampling for target vector t and LDL tree T.
 * tmp[] must have size for at least two polynomials of size 2^logn.
 */
static void
ffSampling_fft(samplerZ samp, void *samp_ctx,
               fpr *z0, fpr *z1,
               const fpr *tree,
               const fpr *t0, const fpr *t1, unsigned logn,
               fpr *tmp) {
    size_t n, hn;
    const fpr *tree0, *tree1;

    /*
     * When logn == 2, we inline the last two recursion levels.
     */
    if (logn == 2) {
        fpr w0, w1, w2, w3, sigma;
        __m128d ww0, ww1, wa, wb, wc, wd;
        __m128d wy0, wy1, wz0, wz1;
        __m128d half, invsqrt8, invsqrt2, neghi, neglo;
        int si0, si1, si2, si3;

        tree0 = tree + 4;
        tree1 = tree + 8;

        half = _mm_set1_pd(0.5);
        invsqrt8 = _mm_set1_pd(0.353553390593273762200422181052);
        invsqrt2 = _mm_set1_pd(0.707106781186547524400844362105);
        neghi = _mm_set_pd(-0.0, 0.0);
        neglo = _mm_set_pd(0.0, -0.0);

        /*
         * We split t1 into w*, then do the recursive invocation,
         * with output in w*. We finally merge back into z1.
         */
        ww0 = _mm_loadu_pd(&t1[0].v);
        ww1 = _mm_loadu_pd(&t1[2].v);
        wa = _mm_unpacklo_pd(ww0, ww1);
        wb = _mm_unpackhi_pd(ww0, ww1);
        wc = _mm_add_pd(wa, wb);
        ww0 = _mm_mul_pd(wc, half);
        wc = _mm_sub_pd(wa, wb);
        wd = _mm_xor_pd(_mm_permute_pd(wc, 1), neghi);
        ww1 = _mm_mul_pd(_mm_add_pd(wc, wd), invsqrt8);

        w2.v = _mm_cvtsd_f64(ww1);
        w3.v = _mm_cvtsd_f64(_mm_permute_pd(ww1, 1));
        wa = ww1;
        sigma = tree1[3];
        si2 = samp(samp_ctx, w2, sigma);
        si3 = samp(samp_ctx, w3, sigma);
        ww1 = _mm_set_pd((double)si3, (double)si2);
        wa = _mm_sub_pd(wa, ww1);
        wb = _mm_loadu_pd(&tree1[0].v);
        wc = _mm_mul_pd(wa, wb);
        wd = _mm_mul_pd(wa, _mm_permute_pd(wb, 1));
        wa = _mm_unpacklo_pd(wc, wd);
        wb = _mm_unpackhi_pd(wc, wd);
        ww0 = _mm_add_pd(ww0, _mm_add_pd(wa, _mm_xor_pd(wb, neglo)));
        w0.v = _mm_cvtsd_f64(ww0);
        w1.v = _mm_cvtsd_f64(_mm_permute_pd(ww0, 1));
        sigma = tree1[2];
        si0 = samp(samp_ctx, w0, sigma);
        si1 = samp(samp_ctx, w1, sigma);
        ww0 = _mm_set_pd((double)si1, (double)si0);

        wc = _mm_mul_pd(
                 _mm_set_pd((double)(si2 + si3), (double)(si2 - si3)),
                 invsqrt2);
        wa = _mm_add_pd(ww0, wc);
        wb = _mm_sub_pd(ww0, wc);
        ww0 = _mm_unpacklo_pd(wa, wb);
        ww1 = _mm_unpackhi_pd(wa, wb);
        _mm_storeu_pd(&z1[0].v, ww0);
        _mm_storeu_pd(&z1[2].v, ww1);

        /*
         * Compute tb0 = t0 + (t1 - z1) * L. Value tb0 ends up in w*.
         */
        wy0 = _mm_sub_pd(_mm_loadu_pd(&t1[0].v), ww0);
        wy1 = _mm_sub_pd(_mm_loadu_pd(&t1[2].v), ww1);
        wz0 = _mm_loadu_pd(&tree[0].v);
        wz1 = _mm_loadu_pd(&tree[2].v);
        ww0 = _mm_sub_pd(_mm_mul_pd(wy0, wz0), _mm_mul_pd(wy1, wz1));
        ww1 = _mm_add_pd(_mm_mul_pd(wy0, wz1), _mm_mul_pd(wy1, wz0));
        ww0 = _mm_add_pd(ww0, _mm_loadu_pd(&t0[0].v));
        ww1 = _mm_add_pd(ww1, _mm_loadu_pd(&t0[2].v));

        /*
         * Second recursive invocation.
         */
        wa = _mm_unpacklo_pd(ww0, ww1);
        wb = _mm_unpackhi_pd(ww0, ww1);
        wc = _mm_add_pd(wa, wb);
        ww0 = _mm_mul_pd(wc, half);
        wc = _mm_sub_pd(wa, wb);
        wd = _mm_xor_pd(_mm_permute_pd(wc, 1), neghi);
        ww1 = _mm_mul_pd(_mm_add_pd(wc, wd), invsqrt8);

        w2.v = _mm_cvtsd_f64(ww1);
        w3.v = _mm_cvtsd_f64(_mm_permute_pd(ww1, 1));
        wa = ww1;
        sigma = tree0[3];
        si2 = samp(samp_ctx, w2, sigma);
        si3 = samp(samp_ctx, w3, sigma);
        ww1 = _mm_set_pd((double)si3, (double)si2);
        wa = _mm_sub_pd(wa, ww1);
        wb = _mm_loadu_pd(&tree0[0].v);
        wc = _mm_mul_pd(wa, wb);
        wd = _mm_mul_pd(wa, _mm_permute_pd(wb, 1));
        wa = _mm_unpacklo_pd(wc, wd);
        wb = _mm_unpackhi_pd(wc, wd);
        ww0 = _mm_add_pd(ww0, _mm_add_pd(wa, _mm_xor_pd(wb, neglo)));
        w0.v = _mm_cvtsd_f64(ww0);
        w1.v = _mm_cvtsd_f64(_mm_permute_pd(ww0, 1));
        sigma = tree0[2];
        si0 = samp(samp_ctx, w0, sigma);
        si1 = samp(samp_ctx, w1, sigma);
        ww0 = _mm_set_pd((double)si1, (double)si0);

        wc = _mm_mul_pd(
                 _mm_set_pd((double)(si2 + si3), (double)(si2 - si3)),
                 invsqrt2);
        wa = _mm_add_pd(ww0, wc);
        wb = _mm_sub_pd(ww0, wc);
        ww0 = _mm_unpacklo_pd(wa, wb);
        ww1 = _mm_unpackhi_pd(wa, wb);
        _mm_storeu_pd(&z0[0].v, ww0);
        _mm_storeu_pd(&z0[2].v, ww1);

        return;
    }

    /*
     * Case logn == 1 is reachable only when using Falcon-2 (the
     * smallest size for which Falcon is mathematically defined, but
     * of course way too insecure to be of any use).
     */
    if (logn == 1) {
        fpr x0, x1, y0, y1, sigma;
        fpr a_re, a_im, b_re, b_im, c_re, c_im;

        x0 = t1[0];
        x1 = t1[1];
        sigma = tree[3];
        z1[0] = y0 = fpr_of(samp(samp_ctx, x0, sigma));
        z1[1] = y1 = fpr_of(samp(samp_ctx, x1, sigma));
        a_re = fpr_sub(x0, y0);
        a_im = fpr_sub(x1, y1);
        b_re = tree[0];
        b_im = tree[1];
        c_re = fpr_sub(fpr_mul(a_re, b_re), fpr_mul(a_im, b_im));
        c_im = fpr_add(fpr_mul(a_re, b_im), fpr_mul(a_im, b_re));
        x0 = fpr_add(c_re, t0[0]);
        x1 = fpr_add(c_im, t0[1]);
        sigma = tree[2];
        z0[0] = fpr_of(samp(samp_ctx, x0, sigma));
        z0[1] = fpr_of(samp(samp_ctx, x1, sigma));

        return;
    }

    /*
     * Normal end of recursion is for logn == 0. Since the last
     * steps of the recursions were inlined in the blocks above
     * (when logn == 1 or 2), this case is not reachable, and is
     * retained here only for documentation purposes.

    if (logn == 0) {
        fpr x0, x1, sigma;

        x0 = t0[0];
        x1 = t1[0];
        sigma = tree[0];
        z0[0] = fpr_of(samp(samp_ctx, x0, sigma));
        z1[0] = fpr_of(samp(samp_ctx, x1, sigma));
        return;
    }

     */

    /*
     * General recursive case (logn >= 3).
     */

    n = (size_t)1 << logn;
    hn = n >> 1;
    tree0 = tree + n;
    tree1 = tree + n + ffLDL_treesize(logn - 1);

    /*
     * We split t1 into z1 (reused as temporary storage), then do
     * the recursive invocation, with output in tmp. We finally
     * merge back into z1.
     */
    PQCLEAN_FALCON512_AVX2_poly_split_fft(z1, z1 + hn, t1, logn);
    ffSampling_fft(samp, samp_ctx, tmp, tmp + hn,
                   tree1, z1, z1 + hn, logn - 1, tmp + n);
    PQCLEAN_FALCON512_AVX2_poly_merge_fft(z1, tmp, tmp + hn, logn);

    /*
     * Compute tb0 = t0 + (t1 - z1) * L. Value tb0 ends up in tmp[].
     */
    memcpy(tmp, t1, n * sizeof * t1);
    PQCLEAN_FALCON512_AVX2_poly_sub(tmp, z1, logn);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(tmp, tree, logn);
    PQCLEAN_FALCON512_AVX2_poly_add(tmp, t0, logn);

    /*
     * Second recursive invocation.
     */
    PQCLEAN_FALCON512_AVX2_poly_split_fft(z0, z0 + hn, tmp, logn);
    ffSampling_fft(samp, samp_ctx, tmp, tmp + hn,
                   tree0, z0, z0 + hn, logn - 1, tmp + n);
    PQCLEAN_FALCON512_AVX2_poly_merge_fft(z0, tmp, tmp + hn, logn);
}

/*
 * Compute a signature: the signature contains two vectors, s1 and s2.
 * The s1 vector is not returned. The squared norm of (s1,s2) is
 * computed, and if it is short enough, then s2 is returned into the
 * s2[] buffer, and 1 is returned; otherwise, s2[] is untouched and 0 is
 * returned; the caller should then try again. This function uses an
 * expanded key.
 *
 * tmp[] must have room for at least six polynomials.
 */
static int
do_sign_tree(samplerZ samp, void *samp_ctx, int16_t *s2,
             const fpr *expanded_key,
             const uint16_t *hm,
             unsigned logn, fpr *tmp) {
    size_t n, u;
    fpr *t0, *t1, *tx, *ty;
    const fpr *b00, *b01, *b10, *b11, *tree;
    fpr ni;
    uint32_t sqn, ng;
    int16_t *s1tmp, *s2tmp;

    n = MKN(logn);
    t0 = tmp;
    t1 = t0 + n;
    b00 = expanded_key + skoff_b00(logn);
    b01 = expanded_key + skoff_b01(logn);
    b10 = expanded_key + skoff_b10(logn);
    b11 = expanded_key + skoff_b11(logn);
    tree = expanded_key + skoff_tree(logn);

    /*
     * Set the target vector to [hm, 0] (hm is the hashed message).
     */
    for (u = 0; u < n; u ++) {
        t0[u] = fpr_of(hm[u]);
        /* This is implicit.
        t1[u] = fpr_zero;
        */
    }

    /*
     * Apply the lattice basis to obtain the real target
     * vector (after normalization with regards to modulus).
     */
    PQCLEAN_FALCON512_AVX2_FFT(t0, logn);
    ni = fpr_inverse_of_q;
    memcpy(t1, t0, n * sizeof * t0);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(t1, b01, logn);
    PQCLEAN_FALCON512_AVX2_poly_mulconst(t1, fpr_neg(ni), logn);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(t0, b11, logn);
    PQCLEAN_FALCON512_AVX2_poly_mulconst(t0, ni, logn);

    tx = t1 + n;
    ty = tx + n;

    /*
     * Apply sampling. Output is written back in [tx, ty].
     */
    ffSampling_fft(samp, samp_ctx, tx, ty, tree, t0, t1, logn, ty + n);

    /*
     * Get the lattice point corresponding to that tiny vector.
     */
    memcpy(t0, tx, n * sizeof * tx);
    memcpy(t1, ty, n * sizeof * ty);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(tx, b00, logn);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(ty, b10, logn);
    PQCLEAN_FALCON512_AVX2_poly_add(tx, ty, logn);
    memcpy(ty, t0, n * sizeof * t0);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(ty, b01, logn);

    memcpy(t0, tx, n * sizeof * tx);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(t1, b11, logn);
    PQCLEAN_FALCON512_AVX2_poly_add(t1, ty, logn);

    PQCLEAN_FALCON512_AVX2_iFFT(t0, logn);
    PQCLEAN_FALCON512_AVX2_iFFT(t1, logn);

    /*
     * Compute the signature.
     */
    s1tmp = (int16_t *)tx;
    sqn = 0;
    ng = 0;
    for (u = 0; u < n; u ++) {
        int32_t z;

        z = (int32_t)hm[u] - (int32_t)fpr_rint(t0[u]);
        sqn += (uint32_t)(z * z);
        ng |= sqn;
        s1tmp[u] = (int16_t)z;
    }
    sqn |= -(ng >> 31);

    /*
     * With "normal" degrees (e.g. 512 or 1024), it is very
     * improbable that the computed vector is not short enough;
     * however, it may happen in practice for the very reduced
     * versions (e.g. degree 16 or below). In that case, the caller
     * will loop, and we must not write anything into s2[] because
     * s2[] may overlap with the hashed message hm[] and we need
     * hm[] for the next iteration.
     */
    s2tmp = (int16_t *)tmp;
    for (u = 0; u < n; u ++) {
        s2tmp[u] = (int16_t) - fpr_rint(t1[u]);
    }
    if (PQCLEAN_FALCON512_AVX2_is_short_half(sqn, s2tmp, logn)) {
        memcpy(s2, s2tmp, n * sizeof * s2);
        memcpy(tmp, s1tmp, n * sizeof * s1tmp);
        return 1;
    }
    return 0;
}

/*
 * Compute a signature: the signature contains two vectors, s1 and s2.
 * The s1 vector is not returned. The squared norm of (s1,s2) is
 * computed, and if it is short enough, then s2 is returned into the
 * s2[] buffer, and 1 is returned; otherwise, s2[] is untouched and 0 is
 * returned; the caller should then try again.
 *
 * tmp[] must have room for at least nine polynomials.
 */
static int
do_sign_dyn(samplerZ samp, void *samp_ctx, int16_t *s2,
            const int8_t *f, const int8_t *g,
            const int8_t *F, const int8_t *G,
            const uint16_t *hm, unsigned logn, fpr *tmp) {
    size_t n, u;
    fpr *t0, *t1, *tx, *ty;
    fpr *b00, *b01, *b10, *b11, *g00, *g01, *g11;
    fpr ni;
    uint32_t sqn, ng;
    int16_t *s1tmp, *s2tmp;

    n = MKN(logn);

    /*
     * Lattice basis is B = [[g, -f], [G, -F]]. We convert it to FFT.
     */
    b00 = tmp;
    b01 = b00 + n;
    b10 = b01 + n;
    b11 = b10 + n;
    smallints_to_fpr(b01, f, logn);
    smallints_to_fpr(b00, g, logn);
    smallints_to_fpr(b11, F, logn);
    smallints_to_fpr(b10, G, logn);
    PQCLEAN_FALCON512_AVX2_FFT(b01, logn);
    PQCLEAN_FALCON512_AVX2_FFT(b00, logn);
    PQCLEAN_FALCON512_AVX2_FFT(b11, logn);
    PQCLEAN_FALCON512_AVX2_FFT(b10, logn);
    PQCLEAN_FALCON512_AVX2_poly_neg(b01, logn);
    PQCLEAN_FALCON512_AVX2_poly_neg(b11, logn);

    /*
     * Compute the Gram matrix G = B·B*. Formulas are:
     *   g00 = b00*adj(b00) + b01*adj(b01)
     *   g01 = b00*adj(b10) + b01*adj(b11)
     *   g10 = b10*adj(b00) + b11*adj(b01)
     *   g11 = b10*adj(b10) + b11*adj(b11)
     *
     * For historical reasons, this implementation uses
     * g00, g01 and g11 (upper triangle). g10 is not kept
     * since it is equal to adj(g01).
     *
     * We _replace_ the matrix B with the Gram matrix, but we
     * must keep b01 and b11 for computing the target vector.
     */
    t0 = b11 + n;
    t1 = t0 + n;

    memcpy(t0, b01, n * sizeof * b01);
    PQCLEAN_FALCON512_AVX2_poly_mulselfadj_fft(t0, logn);    // t0 <- b01*adj(b01)

    memcpy(t1, b00, n * sizeof * b00);
    PQCLEAN_FALCON512_AVX2_poly_muladj_fft(t1, b10, logn);   // t1 <- b00*adj(b10)
    PQCLEAN_FALCON512_AVX2_poly_mulselfadj_fft(b00, logn);   // b00 <- b00*adj(b00)
    PQCLEAN_FALCON512_AVX2_poly_add(b00, t0, logn);      // b00 <- g00
    memcpy(t0, b01, n * sizeof * b01);
    PQCLEAN_FALCON512_AVX2_poly_muladj_fft(b01, b11, logn);  // b01 <- b01*adj(b11)
    PQCLEAN_FALCON512_AVX2_poly_add(b01, t1, logn);      // b01 <- g01

    PQCLEAN_FALCON512_AVX2_poly_mulselfadj_fft(b10, logn);   // b10 <- b10*adj(b10)
    memcpy(t1, b11, n * sizeof * b11);
    PQCLEAN_FALCON512_AVX2_poly_mulselfadj_fft(t1, logn);    // t1 <- b11*adj(b11)
    PQCLEAN_FALCON512_AVX2_poly_add(b10, t1, logn);      // b10 <- g11

    /*
     * We rename variables to make things clearer. The three elements
     * of the Gram matrix uses the first 3*n slots of tmp[], followed
     * by b11 and b01 (in that order).
     */
    g00 = b00;
    g01 = b01;
    g11 = b10;
    b01 = t0;
    t0 = b01 + n;
    t1 = t0 + n;

    /*
     * Memory layout at that point:
     *   g00 g01 g11 b11 b01 t0 t1
     */

    /*
     * Set the target vector to [hm, 0] (hm is the hashed message).
     */
    for (u = 0; u < n; u ++) {
        t0[u] = fpr_of(hm[u]);
        /* This is implicit.
        t1[u] = fpr_zero;
        */
    }

    /*
     * Apply the lattice basis to obtain the real target
     * vector (after normalization with regards to modulus).
     */
    PQCLEAN_FALCON512_AVX2_FFT(t0, logn);
    ni = fpr_inverse_of_q;
    memcpy(t1, t0, n * sizeof * t0);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(t1, b01, logn);
    PQCLEAN_FALCON512_AVX2_poly_mulconst(t1, fpr_neg(ni), logn);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(t0, b11, logn);
    PQCLEAN_FALCON512_AVX2_poly_mulconst(t0, ni, logn);

    /*
     * b01 and b11 can be discarded, so we move back (t0,t1).
     * Memory layout is now:
     *      g00 g01 g11 t0 t1
     */
    memcpy(b11, t0, n * 2 * sizeof * t0);
    t0 = g11 + n;
    t1 = t0 + n;

    /*
     * Apply sampling; result is written over (t0,t1).
     */
    ffSampling_fft_dyntree(samp, samp_ctx,
                           t0, t1, g00, g01, g11, logn, t1 + n);

    /*
     * We arrange the layout back to:
     *     b00 b01 b10 b11 t0 t1
     *
     * We did not conserve the matrix basis, so we must recompute
     * it now.
     */
    b00 = tmp;
    b01 = b00 + n;
    b10 = b01 + n;
    b11 = b10 + n;
    memmove(b11 + n, t0, n * 2 * sizeof * t0);
    t0 = b11 + n;
    t1 = t0 + n;
    smallints_to_fpr(b01, f, logn);
    smallints_to_fpr(b00, g, logn);
    smallints_to_fpr(b11, F, logn);
    smallints_to_fpr(b10, G, logn);
    PQCLEAN_FALCON512_AVX2_FFT(b01, logn);
    PQCLEAN_FALCON512_AVX2_FFT(b00, logn);
    PQCLEAN_FALCON512_AVX2_FFT(b11, logn);
    PQCLEAN_FALCON512_AVX2_FFT(b10, logn);
    PQCLEAN_FALCON512_AVX2_poly_neg(b01, logn);
    PQCLEAN_FALCON512_AVX2_poly_neg(b11, logn);
    tx = t1 + n;
    ty = tx + n;

    /*
     * Get the lattice point corresponding to that tiny vector.
     */
    memcpy(tx, t0, n * sizeof * t0);
    memcpy(ty, t1, n * sizeof * t1);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(tx, b00, logn);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(ty, b10, logn);
    PQCLEAN_FALCON512_AVX2_poly_add(tx, ty, logn);
    memcpy(ty, t0, n * sizeof * t0);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(ty, b01, logn);

    memcpy(t0, tx, n * sizeof * tx);
    PQCLEAN_FALCON512_AVX2_poly_mul_fft(t1, b11, logn);
    PQCLEAN_FALCON512_AVX2_poly_add(t1, ty, logn);
    PQCLEAN_FALCON512_AVX2_iFFT(t0, logn);
    PQCLEAN_FALCON512_AVX2_iFFT(t1, logn);

    s1tmp = (int16_t *)tx;
    sqn = 0;
    ng = 0;
    for (u = 0; u < n; u ++) {
        int32_t z;

        z = (int32_t)hm[u] - (int32_t)fpr_rint(t0[u]);
        sqn += (uint32_t)(z * z);
        ng |= sqn;
        s1tmp[u] = (int16_t)z;
    }
    sqn |= -(ng >> 31);

    /*
     * With "normal" degrees (e.g. 512 or 1024), it is very
     * improbable that the computed vector is not short enough;
     * however, it may happen in practice for the very reduced
     * versions (e.g. degree 16 or below). In that case, the caller
     * will loop, and we must not write anything into s2[] because
     * s2[] may overlap with the hashed message hm[] and we need
     * hm[] for the next iteration.
     */
    s2tmp = (int16_t *)tmp;
    for (u = 0; u < n; u ++) {
        s2tmp[u] = (int16_t) - fpr_rint(t1[u]);
    }
    if (PQCLEAN_FALCON512_AVX2_is_short_half(sqn, s2tmp, logn)) {
        memcpy(s2, s2tmp, n * sizeof * s2);
        memcpy(tmp, s1tmp, n * sizeof * s1tmp);
        return 1;
    }
    return 0;
}

/*
 * Sample an integer value along a half-gaussian distribution centered
 * on zero and standard deviation 1.8205, with a precision of 72 bits.
 */
int
PQCLEAN_FALCON512_AVX2_gaussian0_sampler(prng *p) {

    /*
     * High words.
     */
    static const union {
        uint16_t u16[16];
        __m256i ymm[1];
    } rhi15 = {
        {
            0x51FB, 0x2A69, 0x113E, 0x0568,
            0x014A, 0x003B, 0x0008, 0x0000,
            0x0000, 0x0000, 0x0000, 0x0000,
            0x0000, 0x0000, 0x0000, 0x0000
        }
    };

    static const union {
        uint64_t u64[20];
        __m256i ymm[5];
    } rlo57 = {
        {
            0x1F42ED3AC391802, 0x12B181F3F7DDB82,
            0x1CDD0934829C1FF, 0x1754377C7994AE4,
            0x1846CAEF33F1F6F, 0x14AC754ED74BD5F,
            0x024DD542B776AE4, 0x1A1FFDC65AD63DA,
            0x01F80D88A7B6428, 0x001C3FDB2040C69,
            0x00012CF24D031FB, 0x00000949F8B091F,
            0x0000003665DA998, 0x00000000EBF6EBB,
            0x0000000002F5D7E, 0x000000000007098,
            0x0000000000000C6, 0x000000000000001,
            0x000000000000000, 0x000000000000000
        }
    };

    uint64_t lo;
    unsigned hi;
    __m256i xhi, rhi, gthi, eqhi, eqm;
    __m256i xlo, gtlo0, gtlo1, gtlo2, gtlo3, gtlo4;
    __m128i t, zt;
    int r;

    /*
     * Get a 72-bit random value and split it into a low part
     * (57 bits) and a high part (15 bits)
     */
    lo = prng_get_u64(p);
    hi = prng_get_u8(p);
    hi = (hi << 7) | (unsigned)(lo >> 57);
    lo &= 0x1FFFFFFFFFFFFFF;

    /*
     * Broadcast the high part and compare it with the relevant
     * values. We need both a "greater than" and an "equal"
     * comparisons.
     */
    xhi = _mm256_broadcastw_epi16(_mm_cvtsi32_si128((int32_t)hi));
    rhi = _mm256_loadu_si256(&rhi15.ymm[0]);
    gthi = _mm256_cmpgt_epi16(rhi, xhi);
    eqhi = _mm256_cmpeq_epi16(rhi, xhi);

    /*
     * The result is the number of 72-bit values (among the list of 19)
     * which are greater than the 72-bit random value. We first count
     * all non-zero 16-bit elements in the first eight of gthi. Such
     * elements have value -1 or 0, so we first negate them.
     */
    t = _mm_srli_epi16(_mm256_castsi256_si128(gthi), 15);
    zt = _mm_setzero_si128();
    t = _mm_hadd_epi16(t, zt);
    t = _mm_hadd_epi16(t, zt);
    t = _mm_hadd_epi16(t, zt);
    r = _mm_cvtsi128_si32(t);

    /*
     * We must look at the low bits for all values for which the
     * high bits are an "equal" match; values 8-18 all have the
     * same high bits (0).
     * On 32-bit systems, 'lo' really is two registers, requiring
     * some extra code.
     */
    xlo = _mm256_broadcastq_epi64(_mm_cvtsi64_si128(*(int64_t *)&lo));
    gtlo0 = _mm256_cmpgt_epi64(_mm256_loadu_si256(&rlo57.ymm[0]), xlo);
    gtlo1 = _mm256_cmpgt_epi64(_mm256_loadu_si256(&rlo57.ymm[1]), xlo);
    gtlo2 = _mm256_cmpgt_epi64(_mm256_loadu_si256(&rlo57.ymm[2]), xlo);
    gtlo3 = _mm256_cmpgt_epi64(_mm256_loadu_si256(&rlo57.ymm[3]), xlo);
    gtlo4 = _mm256_cmpgt_epi64(_mm256_loadu_si256(&rlo57.ymm[4]), xlo);

    /*
     * Keep only comparison results that correspond to the non-zero
     * elements in eqhi.
     */
    gtlo0 = _mm256_and_si256(gtlo0, _mm256_cvtepi16_epi64(
                                 _mm256_castsi256_si128(eqhi)));
    gtlo1 = _mm256_and_si256(gtlo1, _mm256_cvtepi16_epi64(
                                 _mm256_castsi256_si128(_mm256_bsrli_epi128(eqhi, 8))));
    eqm = _mm256_permute4x64_epi64(eqhi, 0xFF);
    gtlo2 = _mm256_and_si256(gtlo2, eqm);
    gtlo3 = _mm256_and_si256(gtlo3, eqm);
    gtlo4 = _mm256_and_si256(gtlo4, eqm);

    /*
     * Add all values to count the total number of "-1" elements.
     * Since the first eight "high" words are all different, only
     * one element (at most) in gtlo0:gtlo1 can be non-zero; however,
     * if the high word of the random value is zero, then many
     * elements of gtlo2:gtlo3:gtlo4 can be non-zero.
     */
    gtlo0 = _mm256_or_si256(gtlo0, gtlo1);
    gtlo0 = _mm256_add_epi64(
                _mm256_add_epi64(gtlo0, gtlo2),
                _mm256_add_epi64(gtlo3, gtlo4));
    t = _mm_add_epi64(
            _mm256_castsi256_si128(gtlo0),
            _mm256_extracti128_si256(gtlo0, 1));
    t = _mm_add_epi64(t, _mm_srli_si128(t, 8));
    r -= _mm_cvtsi128_si32(t);

    return r;

}

/*
 * Sample a bit with probability exp(-x) for some x >= 0.
 */
static int
BerExp(prng *p, fpr x, fpr ccs) {
    int s, i;
    fpr r;
    uint32_t sw, w;
    uint64_t z;

    /*
     * Reduce x modulo log(2): x = s*log(2) + r, with s an integer,
     * and 0 <= r < log(2). Since x >= 0, we can use fpr_trunc().
     */
    s = (int)fpr_trunc(fpr_mul(x, fpr_inv_log2));
    r = fpr_sub(x, fpr_mul(fpr_of(s), fpr_log2));

    /*
     * It may happen (quite rarely) that s >= 64; if sigma = 1.2
     * (the minimum value for sigma), r = 0 and b = 1, then we get
     * s >= 64 if the half-Gaussian produced a z >= 13, which happens
     * with probability about 0.000000000230383991, which is
     * approximatively equal to 2^(-32). In any case, if s >= 64,
     * then BerExp will be non-zero with probability less than
     * 2^(-64), so we can simply saturate s at 63.
     */
    sw = (uint32_t)s;
    sw ^= (sw ^ 63) & -((63 - sw) >> 31);
    s = (int)sw;

    /*
     * Compute exp(-r); we know that 0 <= r < log(2) at this point, so
     * we can use fpr_expm_p63(), which yields a result scaled to 2^63.
     * We scale it up to 2^64, then right-shift it by s bits because
     * we really want exp(-x) = 2^(-s)*exp(-r).
     *
     * The "-1" operation makes sure that the value fits on 64 bits
     * (i.e. if r = 0, we may get 2^64, and we prefer 2^64-1 in that
     * case). The bias is negligible since fpr_expm_p63() only computes
     * with 51 bits of precision or so.
     */
    z = ((fpr_expm_p63(r, ccs) << 1) - 1) >> s;

    /*
     * Sample a bit with probability exp(-x). Since x = s*log(2) + r,
     * exp(-x) = 2^-s * exp(-r), we compare lazily exp(-x) with the
     * PRNG output to limit its consumption, the sign of the difference
     * yields the expected result.
     */
    i = 64;
    do {
        i -= 8;
        w = prng_get_u8(p) - ((uint32_t)(z >> i) & 0xFF);
    } while (!w && i > 0);
    return (int)(w >> 31);
}

/*
 * The sampler produces a random integer that follows a discrete Gaussian
 * distribution, centered on mu, and with standard deviation sigma. The
 * provided parameter isigma is equal to 1/sigma.
 *
 * The value of sigma MUST lie between 1 and 2 (i.e. isigma lies between
 * 0.5 and 1); in Falcon, sigma should always be between 1.2 and 1.9.
 */
int
PQCLEAN_FALCON512_AVX2_sampler(void *ctx, fpr mu, fpr isigma) {
    sampler_context *spc;
    int s, z0, z, b;
    fpr r, dss, ccs, x;

    spc = ctx;

    /*
     * Center is mu. We compute mu = s + r where s is an integer
     * and 0 <= r < 1.
     */
    s = (int)fpr_floor(mu);
    r = fpr_sub(mu, fpr_of(s));

    /*
     * dss = 1/(2*sigma^2) = 0.5*(isigma^2).
     */
    dss = fpr_half(fpr_sqr(isigma));

    /*
     * ccs = sigma_min / sigma = sigma_min * isigma.
     */
    ccs = fpr_mul(isigma, spc->sigma_min);

    /*
     * We now need to sample on center r.
     */
    for (;;) {
        /*
         * Sample z for a Gaussian distribution. Then get a
         * random bit b to turn the sampling into a bimodal
         * distribution: if b = 1, we use z+1, otherwise we
         * use -z. We thus have two situations:
         *
         *  - b = 1: z >= 1 and sampled against a Gaussian
         *    centered on 1.
         *  - b = 0: z <= 0 and sampled against a Gaussian
         *    centered on 0.
         */
        z0 = PQCLEAN_FALCON512_AVX2_gaussian0_sampler(&spc->p);
        b = (int)prng_get_u8(&spc->p) & 1;
        z = b + ((b << 1) - 1) * z0;

        /*
         * Rejection sampling. We want a Gaussian centered on r;
         * but we sampled against a Gaussian centered on b (0 or
         * 1). But we know that z is always in the range where
         * our sampling distribution is greater than the Gaussian
         * distribution, so rejection works.
         *
         * We got z with distribution:
         *    G(z) = exp(-((z-b)^2)/(2*sigma0^2))
         * We target distribution:
         *    S(z) = exp(-((z-r)^2)/(2*sigma^2))
         * Rejection sampling works by keeping the value z with
         * probability S(z)/G(z), and starting again otherwise.
         * This requires S(z) <= G(z), which is the case here.
         * Thus, we simply need to keep our z with probability:
         *    P = exp(-x)
         * where:
         *    x = ((z-r)^2)/(2*sigma^2) - ((z-b)^2)/(2*sigma0^2)
         *
         * Here, we scale up the Bernouilli distribution, which
         * makes rejection more probable, but makes rejection
         * rate sufficiently decorrelated from the Gaussian
         * center and standard deviation that the whole sampler
         * can be said to be constant-time.
         */
        x = fpr_mul(fpr_sqr(fpr_sub(fpr_of(z), r)), dss);
        x = fpr_sub(x, fpr_mul(fpr_of(z0 * z0), fpr_inv_2sqrsigma0));
        if (BerExp(&spc->p, x, ccs)) {
            /*
             * Rejection sampling was centered on r, but the
             * actual center is mu = s + r.
             */
            return s + z;
        }
    }
}

/* see inner.h */
void
PQCLEAN_FALCON512_AVX2_sign_tree(int16_t *sig, inner_shake256_context *rng,
                                 const fpr *expanded_key,
                                 const uint16_t *hm, unsigned logn, uint8_t *tmp) {
    fpr *ftmp;

    ftmp = (fpr *)tmp;
    for (;;) {
        /*
         * Signature produces short vectors s1 and s2. The
         * signature is acceptable only if the aggregate vector
         * s1,s2 is short; we must use the same bound as the
         * verifier.
         *
         * If the signature is acceptable, then we return only s2
         * (the verifier recomputes s1 from s2, the hashed message,
         * and the public key).
         */
        sampler_context spc;
        samplerZ samp;
        void *samp_ctx;

        /*
         * Normal sampling. We use a fast PRNG seeded from our
         * SHAKE context ('rng').
         */
        if (logn == 10) {
            spc.sigma_min = fpr_sigma_min_10;
        } else {
            spc.sigma_min = fpr_sigma_min_9;
        }
        PQCLEAN_FALCON512_AVX2_prng_init(&spc.p, rng);
        samp = PQCLEAN_FALCON512_AVX2_sampler;
        samp_ctx = &spc;

        /*
         * Do the actual signature.
         */
        if (do_sign_tree(samp, samp_ctx, sig,
                         expanded_key, hm, logn, ftmp)) {
            break;
        }
    }
}

/* see inner.h */
void
PQCLEAN_FALCON512_AVX2_sign_dyn(int16_t *sig, inner_shake256_context *rng,
                                const int8_t *f, const int8_t *g,
                                const int8_t *F, const int8_t *G,
                                const uint16_t *hm, unsigned logn, uint8_t *tmp) {
    fpr *ftmp;

    ftmp = (fpr *)tmp;
    for (;;) {
        /*
         * Signature produces short vectors s1 and s2. The
         * signature is acceptable only if the aggregate vector
         * s1,s2 is short; we must use the same bound as the
         * verifier.
         *
         * If the signature is acceptable, then we return only s2
         * (the verifier recomputes s1 from s2, the hashed message,
         * and the public key).
         */
        sampler_context spc;
        samplerZ samp;
        void *samp_ctx;

        /*
         * Normal sampling. We use a fast PRNG seeded from our
         * SHAKE context ('rng').
         */
        if (logn == 10) {
            spc.sigma_min = fpr_sigma_min_10;
        } else {
            spc.sigma_min = fpr_sigma_min_9;
        }
        PQCLEAN_FALCON512_AVX2_prng_init(&spc.p, rng);
        samp = PQCLEAN_FALCON512_AVX2_sampler;
        samp_ctx = &spc;

        /*
         * Do the actual signature.
         */
        if (do_sign_dyn(samp, samp_ctx, sig,
                        f, g, F, G, hm, logn, ftmp)) {
            break;
        }
    }
}
