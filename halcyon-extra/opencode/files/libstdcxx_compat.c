/*
 * SPDX-License-Identifier: MIT
 *
 * Minimal libstdc++ ABI compatibility shim for musl Bun-based binaries.
 *
 * Bun is built against musl and dynamically links libstdc++.so.6, but only
 * imports 28 C++ runtime symbols. This file provides those symbols with the
 * same ABI, using only musl/pthreads and libc++abi. It is not GNU libstdc++.
 */

#define _GNU_SOURCE
#include <pthread.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define EXPORT __attribute__((visibility("default")))

/* ------------------------------------------------------------------ */
/* std::condition_variable                                             */
/* ------------------------------------------------------------------ */

/* libstdc++ stores a pthread_cond_t at offset 0. */

EXPORT void _ZNSt18condition_variableC1Ev(void *self)
    __asm__("_ZNSt18condition_variableC1Ev");
EXPORT void _ZNSt18condition_variableC1Ev(void *self)
{
    pthread_cond_init((pthread_cond_t *)self, NULL);
}

EXPORT void _ZNSt18condition_variableD1Ev(void *self)
    __asm__("_ZNSt18condition_variableD1Ev");
EXPORT void _ZNSt18condition_variableD1Ev(void *self)
{
    pthread_cond_destroy((pthread_cond_t *)self);
}

EXPORT void _ZNSt18condition_variable10notify_oneEv(void *self)
    __asm__("_ZNSt18condition_variable10notify_oneEv");
EXPORT void _ZNSt18condition_variable10notify_oneEv(void *self)
{
    pthread_cond_signal((pthread_cond_t *)self);
}

EXPORT void _ZNSt18condition_variable10notify_allEv(void *self)
    __asm__("_ZNSt18condition_variable10notify_allEv");
EXPORT void _ZNSt18condition_variable10notify_allEv(void *self)
{
    pthread_cond_broadcast((pthread_cond_t *)self);
}

/*
 * std::unique_lock<std::mutex> is { std::mutex *device; bool owns; } on the
 * Itanium ABI. std::mutex contains a pthread_mutex_t at offset 0.
 */
struct unique_lock_layout {
    void *device;
    unsigned char owns;
};

EXPORT void _ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE(
    void *self, void *lockp)
    __asm__("_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE");
EXPORT void _ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE(
    void *self, void *lockp)
{
    struct unique_lock_layout *lock = lockp;
    pthread_cond_wait((pthread_cond_t *)self, (pthread_mutex_t *)lock->device);
}

/* ------------------------------------------------------------------ */
/* std::chrono::steady_clock::now                                      */
/* ------------------------------------------------------------------ */

EXPORT int64_t _ZNSt6chrono3_V212steady_clock3nowEv(void)
    __asm__("_ZNSt6chrono3_V212steady_clock3nowEv");
EXPORT int64_t _ZNSt6chrono3_V212steady_clock3nowEv(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (int64_t)ts.tv_sec * 1000000000LL + ts.tv_nsec;
}

/* ------------------------------------------------------------------ */
/* std::_Hash_bytes                                                    */
/* ------------------------------------------------------------------ */

EXPORT size_t _ZSt11_Hash_bytesPKvmm(const void *ptr, size_t len,
                                     size_t seed)
    __asm__("_ZSt11_Hash_bytesPKvmm");
EXPORT size_t _ZSt11_Hash_bytesPKvmm(const void *ptr, size_t len,
                                     size_t seed)
{
    /* MurmurHash64A, the algorithm libstdc++ uses for _Hash_bytes. */
    const uint64_t m = 0xc6a4a7935bd1e995ULL;
    const int r = 47;
    uint64_t h = (uint64_t)seed ^ ((uint64_t)len * m);
    const unsigned char *data = ptr;
    const unsigned char *end = data + (len & ~(size_t)7);

    while (data != end) {
        uint64_t k;
        memcpy(&k, data, sizeof(k));
        k *= m;
        k ^= k >> r;
        k *= m;
        h ^= k;
        h *= m;
        data += 8;
    }

    switch (len & 7) {
    case 7: h ^= (uint64_t)data[6] << 48; /* fallthrough */
    case 6: h ^= (uint64_t)data[5] << 40; /* fallthrough */
    case 5: h ^= (uint64_t)data[4] << 32; /* fallthrough */
    case 4: h ^= (uint64_t)data[3] << 24; /* fallthrough */
    case 3: h ^= (uint64_t)data[2] << 16; /* fallthrough */
    case 2: h ^= (uint64_t)data[1] << 8;  /* fallthrough */
    case 1: h ^= (uint64_t)data[0]; h *= m;
    }

    h ^= h >> r;
    h *= m;
    h ^= h >> r;
    return (size_t)h;
}

/* ------------------------------------------------------------------ */
/* std::__detail::_Prime_rehash_policy                                 */
/* ------------------------------------------------------------------ */

typedef struct {
    unsigned char first;
    size_t second;
} rehash_result;

EXPORT size_t _ZNKSt8__detail20_Prime_rehash_policy11_M_next_bktEm(
    const void *self, size_t n)
    __asm__("_ZNKSt8__detail20_Prime_rehash_policy11_M_next_bktEm");
EXPORT size_t _ZNKSt8__detail20_Prime_rehash_policy11_M_next_bktEm(
    const void *self, size_t n)
{
    (void)self;
    return n == 0 ? 1 : n;
}

EXPORT rehash_result _ZNKSt8__detail20_Prime_rehash_policy14_M_need_rehashEmmm(
    const void *self, size_t bkt, size_t nelt, size_t nins)
    __asm__("_ZNKSt8__detail20_Prime_rehash_policy14_M_need_rehashEmmm");
EXPORT rehash_result _ZNKSt8__detail20_Prime_rehash_policy14_M_need_rehashEmmm(
    const void *self, size_t bkt, size_t nelt, size_t nins)
{
    rehash_result r = { 0, 0 };
    (void)self;
    (void)bkt;
    (void)nelt;
    (void)nins;
    return r;
}

/* ------------------------------------------------------------------ */
/* std::__detail::_List_node_base                                      */
/* ------------------------------------------------------------------ */

struct list_node {
    struct list_node *next;
    struct list_node *prev;
};

EXPORT void _ZNSt8__detail15_List_node_base7_M_hookEPS0_(
    struct list_node *self, struct list_node *node)
    __asm__("_ZNSt8__detail15_List_node_base7_M_hookEPS0_");
EXPORT void _ZNSt8__detail15_List_node_base7_M_hookEPS0_(
    struct list_node *self, struct list_node *node)
{
    node->next = self;
    node->prev = self->prev;
    self->prev->next = node;
    self->prev = node;
}

EXPORT void _ZNSt8__detail15_List_node_base9_M_unhookEv(
    struct list_node *self)
    __asm__("_ZNSt8__detail15_List_node_base9_M_unhookEv");
EXPORT void _ZNSt8__detail15_List_node_base9_M_unhookEv(
    struct list_node *self)
{
    self->prev->next = self->next;
    self->next->prev = self->prev;
}

/* ------------------------------------------------------------------ */
/* std::_Rb_tree                                                       */
/* ------------------------------------------------------------------ */

struct rb_node {
    int color; /* 0 = red, 1 = black */
    struct rb_node *parent;
    struct rb_node *left;
    struct rb_node *right;
};

static struct rb_node *rb_minimum(struct rb_node *x)
{
    while (x->left)
        x = x->left;
    return x;
}

static struct rb_node *rb_maximum(struct rb_node *x)
{
    while (x->right)
        x = x->right;
    return x;
}

static void rb_rotate_left(struct rb_node *x, struct rb_node **root)
{
    struct rb_node *y = x->right;
    x->right = y->left;
    if (y->left)
        y->left->parent = x;
    y->parent = x->parent;
    if (x == *root)
        *root = y;
    else if (x == x->parent->left)
        x->parent->left = y;
    else
        x->parent->right = y;
    y->left = x;
    x->parent = y;
}

static void rb_rotate_right(struct rb_node *x, struct rb_node **root)
{
    struct rb_node *y = x->left;
    x->left = y->right;
    if (y->right)
        y->right->parent = x;
    y->parent = x->parent;
    if (x == *root)
        *root = y;
    else if (x == x->parent->right)
        x->parent->right = y;
    else
        x->parent->left = y;
    y->right = x;
    x->parent = y;
}

EXPORT struct rb_node *_ZSt18_Rb_tree_incrementPSt18_Rb_tree_node_base(
    struct rb_node *x)
    __asm__("_ZSt18_Rb_tree_incrementPSt18_Rb_tree_node_base");
EXPORT struct rb_node *_ZSt18_Rb_tree_incrementPSt18_Rb_tree_node_base(
    struct rb_node *x)
{
    if (x->right) {
        x = x->right;
        while (x->left)
            x = x->left;
        return x;
    }
    while (x->parent && x == x->parent->right)
        x = x->parent;
    if (x->parent && x->right != x->parent)
        x = x->parent;
    return x;
}

EXPORT struct rb_node *_ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(
    struct rb_node *x)
    __asm__("_ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base");
EXPORT struct rb_node *_ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(
    struct rb_node *x)
{
    if (x->color == 0 && x->parent->parent == x) {
        x = x->right;
    } else if (x->left) {
        x = x->left;
        while (x->right)
            x = x->right;
    } else {
        while (x->parent && x == x->parent->left)
            x = x->parent;
        x = x->parent;
    }
    return x;
}

EXPORT void _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(
    int insert_left, struct rb_node *x, struct rb_node *p,
    struct rb_node *header)
    __asm__("_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_");
EXPORT void _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(
    int insert_left, struct rb_node *x, struct rb_node *p,
    struct rb_node *header)
{
    struct rb_node **root = &header->parent;

    x->color = 0;
    x->parent = p;
    x->left = NULL;
    x->right = NULL;

    if (insert_left) {
        p->left = x;
        if (p == header) {
            header->parent = x;
            header->right = x;
        } else if (p == header->left) {
            header->left = x;
        }
    } else {
        p->right = x;
        if (p == header->right)
            header->right = x;
    }

    while (x != *root && x->parent->color == 0) {
        struct rb_node *xpp = x->parent->parent;
        if (x->parent == xpp->left) {
            struct rb_node *y = xpp->right;
            if (y && y->color == 0) {
                x->parent->color = 1;
                y->color = 1;
                xpp->color = 0;
                x = xpp;
            } else {
                if (x == x->parent->right) {
                    x = x->parent;
                    rb_rotate_left(x, root);
                }
                x->parent->color = 1;
                xpp->color = 0;
                rb_rotate_right(xpp, root);
            }
        } else {
            struct rb_node *y = xpp->left;
            if (y && y->color == 0) {
                x->parent->color = 1;
                y->color = 1;
                xpp->color = 0;
                x = xpp;
            } else {
                if (x == x->parent->left) {
                    x = x->parent;
                    rb_rotate_right(x, root);
                }
                x->parent->color = 1;
                xpp->color = 0;
                rb_rotate_left(xpp, root);
            }
        }
    }

    (*root)->color = 1;
}

EXPORT struct rb_node *_ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_(
    struct rb_node *z, struct rb_node *header)
    __asm__("_ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_");
EXPORT struct rb_node *_ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_(
    struct rb_node *z, struct rb_node *header)
{
    struct rb_node **root = &header->parent;
    struct rb_node **leftmost = &header->left;
    struct rb_node **rightmost = &header->right;
    struct rb_node *y = z;
    struct rb_node *x = NULL;
    struct rb_node *x_parent = NULL;

    if (y->left == NULL) {
        x = y->right;
    } else if (y->right == NULL) {
        x = y->left;
    } else {
        y = rb_minimum(y->right);
        x = y->right;
    }

    if (y != z) {
        z->left->parent = y;
        y->left = z->left;
        if (y != z->right) {
            x_parent = y->parent;
            if (x)
                x->parent = y->parent;
            y->parent->left = x;
            y->right = z->right;
            z->right->parent = y;
        } else {
            x_parent = y;
        }
        if (*root == z)
            *root = y;
        else if (z->parent->left == z)
            z->parent->left = y;
        else
            z->parent->right = y;
        y->parent = z->parent;
        {
            int tmp = y->color;
            y->color = z->color;
            z->color = tmp;
        }
        y = z;
    } else {
        x_parent = y->parent;
        if (x)
            x->parent = y->parent;
        if (*root == z)
            *root = x;
        else if (z->parent->left == z)
            z->parent->left = x;
        else
            z->parent->right = x;
        if (*leftmost == z) {
            if (z->right == NULL)
                *leftmost = z->parent;
            else
                *leftmost = rb_minimum(x);
        }
        if (*rightmost == z) {
            if (z->left == NULL)
                *rightmost = z->parent;
            else
                *rightmost = rb_maximum(x);
        }
    }

    if (y->color != 0) {
        while (x != *root && (!x || x->color == 1)) {
            if (x == x_parent->left) {
                struct rb_node *w = x_parent->right;
                if (w->color == 0) {
                    w->color = 1;
                    x_parent->color = 0;
                    rb_rotate_left(x_parent, root);
                    w = x_parent->right;
                }
                if ((!w->left || w->left->color == 1) &&
                    (!w->right || w->right->color == 1)) {
                    w->color = 0;
                    x = x_parent;
                    x_parent = x_parent->parent;
                } else {
                    if (!w->right || w->right->color == 1) {
                        if (w->left)
                            w->left->color = 1;
                        w->color = 0;
                        rb_rotate_right(w, root);
                        w = x_parent->right;
                    }
                    w->color = x_parent->color;
                    x_parent->color = 1;
                    if (w->right)
                        w->right->color = 1;
                    rb_rotate_left(x_parent, root);
                    break;
                }
            } else {
                struct rb_node *w = x_parent->left;
                if (w->color == 0) {
                    w->color = 1;
                    x_parent->color = 0;
                    rb_rotate_right(x_parent, root);
                    w = x_parent->left;
                }
                if ((!w->right || w->right->color == 1) &&
                    (!w->left || w->left->color == 1)) {
                    w->color = 0;
                    x = x_parent;
                    x_parent = x_parent->parent;
                } else {
                    if (!w->left || w->left->color == 1) {
                        if (w->right)
                            w->right->color = 1;
                        w->color = 0;
                        rb_rotate_left(w, root);
                        w = x_parent->left;
                    }
                    w->color = x_parent->color;
                    x_parent->color = 1;
                    if (w->left)
                        w->left->color = 1;
                    rb_rotate_right(x_parent, root);
                    break;
                }
            }
        }
        if (x)
            x->color = 1;
    }

    return y;
}

/* ------------------------------------------------------------------ */
/* call_once / TLS state                                               */
/* ------------------------------------------------------------------ */

EXPORT __thread void *__once_callable
    __asm__("_ZSt15__once_callable") = NULL;
EXPORT __thread void (*__once_call)(void)
    __asm__("_ZSt11__once_call") = NULL;

EXPORT void __once_proxy(void) __asm__("__once_proxy");
EXPORT void __once_proxy(void)
{
    if (__once_call)
        __once_call();
}

/* ------------------------------------------------------------------ */
/* terminate / exception helpers                                       */
/* ------------------------------------------------------------------ */

typedef void (*term_handler)(void);

static term_handler terminate_handler = NULL;

EXPORT term_handler _ZSt13set_terminatePFvvE(term_handler h)
    __asm__("_ZSt13set_terminatePFvvE");
EXPORT term_handler _ZSt13set_terminatePFvvE(term_handler h)
{
    term_handler old = terminate_handler;
    terminate_handler = h;
    return old;
}

EXPORT term_handler _ZSt15get_new_handlerv(void)
    __asm__("_ZSt15get_new_handlerv");
EXPORT term_handler _ZSt15get_new_handlerv(void)
{
    return NULL;
}

EXPORT void _ZSt9terminatev(void) __asm__("_ZSt9terminatev");
EXPORT void _ZSt9terminatev(void)
{
    if (terminate_handler)
        terminate_handler();
    abort();
}

EXPORT void _ZSt17__throw_bad_allocv(void)
    __asm__("_ZSt17__throw_bad_allocv");
EXPORT void _ZSt17__throw_bad_allocv(void)
{
    _ZSt9terminatev();
}

EXPORT void _ZSt19__throw_logic_errorPKc(const char *msg)
    __asm__("_ZSt19__throw_logic_errorPKc");
EXPORT void _ZSt19__throw_logic_errorPKc(const char *msg)
{
    (void)msg;
    _ZSt9terminatev();
}

EXPORT void _ZSt20__throw_length_errorPKc(const char *msg)
    __asm__("_ZSt20__throw_length_errorPKc");
EXPORT void _ZSt20__throw_length_errorPKc(const char *msg)
{
    (void)msg;
    _ZSt9terminatev();
}

EXPORT void _ZSt20__throw_system_errori(int err)
    __asm__("_ZSt20__throw_system_errori");
EXPORT void _ZSt20__throw_system_errori(int err)
{
    (void)err;
    _ZSt9terminatev();
}

EXPORT void _ZSt24__throw_out_of_range_fmtPKcz(const char *fmt, ...)
    __asm__("_ZSt24__throw_out_of_range_fmtPKcz");
EXPORT void _ZSt24__throw_out_of_range_fmtPKcz(const char *fmt, ...)
{
    (void)fmt;
    _ZSt9terminatev();
}

EXPORT void _ZSt25__throw_bad_function_callv(void)
    __asm__("_ZSt25__throw_bad_function_callv");
EXPORT void _ZSt25__throw_bad_function_callv(void)
{
    _ZSt9terminatev();
}

EXPORT void _ZSt28__throw_bad_array_new_lengthv(void)
    __asm__("_ZSt28__throw_bad_array_new_lengthv");
EXPORT void _ZSt28__throw_bad_array_new_lengthv(void)
{
    _ZSt9terminatev();
}

EXPORT void _ZSt21__glibcxx_assert_failPKciS0_S0_(
    const char *file, int line, const char *func, const char *msg)
    __asm__("_ZSt21__glibcxx_assert_failPKciS0_S0_");
EXPORT void _ZSt21__glibcxx_assert_failPKciS0_S0_(
    const char *file, int line, const char *func, const char *msg)
{
    (void)file;
    (void)line;
    (void)func;
    (void)msg;
    _ZSt9terminatev();
}
