// Compatibility shim for the prebuilt TorrHunt binary.
//
// The binary is built against libstdc++ (glibc toolchain) while Chimera's Qt 6
// is built against libc++. Most Qt symbols are unaffected because they only
// use Qt types, but a handful of Qt APIs take std:: types (std::function,
// std::optional and std::chrono::nanoseconds) and therefore have a
// different symbol mangling. This shim provides the libstdc++-mangled
// symbols and forwards them to the libc++-mangled Qt implementations.

#include <QDir>
#include <QObject>
#include <QTimer>
#include <QVariant>
#include <QWebEngineFindTextResult>
#include <QWebEnginePage>

#include <chrono>
#include <cstring>
#include <functional>
#include <optional>
#include <utility>

namespace {

// libstdc++'s std::function layout (see bits/std_function.h).
//
//   struct _Any_data { union { ... }; };  // 16 bytes
//   class _Function_base {
//       _Any_data _M_functor;
//       bool (*_M_manager)(_Any_data &, const _Any_data &, _Manager_operation);
//   };
//   class function<R(Args...)> : public _Function_base {
//       R (*_M_invoker)(const _Any_data &, Args &&...);
//   };
//
// _Manager_operation: __get_type_info, __get_functor_ptr,
// __clone_functor (2), __destroy_functor (3).
struct AnyData {
    alignas(16) unsigned char data[16];
};

using ManagerType = bool (*)(AnyData &, const AnyData &, int);

template <typename Invoker>
struct FunctionLayout {
    AnyData functor;
    ManagerType manager;
    Invoker invoker;
};

// Owns a copy of a libstdc++ std::function and exposes it as a normal
// callable object, so it can be stored in a libc++ std::function.
template <typename Invoker, typename... Args>
class FunctionWrapper {
public:
    explicit FunctionWrapper(const void *src) {
        auto *layout = static_cast<const FunctionLayout<Invoker> *>(src);
        manager_ = layout->manager;
        invoker_ = layout->invoker;
        if (manager_)
            manager_(functor_, layout->functor, 2);
        else
            std::memset(&functor_, 0, sizeof(functor_));
    }

    FunctionWrapper(const FunctionWrapper &other) {
        manager_ = other.manager_;
        invoker_ = other.invoker_;
        if (manager_)
            manager_(functor_, other.functor_, 2);
        else
            std::memset(&functor_, 0, sizeof(functor_));
    }

    FunctionWrapper(FunctionWrapper &&other) noexcept {
        manager_ = other.manager_;
        invoker_ = other.invoker_;
        std::memcpy(&functor_, &other.functor_, sizeof(functor_));
        other.manager_ = nullptr;
        other.invoker_ = nullptr;
    }

    FunctionWrapper &operator=(const FunctionWrapper &) = delete;

    ~FunctionWrapper() {
        if (manager_)
            manager_(functor_, functor_, 3);
    }

    void operator()(Args... args) const {
        if (invoker_)
            invoker_(functor_, args...);
    }

private:
    AnyData functor_;
    ManagerType manager_;
    Invoker invoker_;
};

using FindTextInvoker = void (*)(
    const AnyData &, const QWebEngineFindTextResult &
);
using VariantInvoker = void (*)(const AnyData &, const QVariant &);

} // namespace

extern "C" void torrhunt_find_text(
    QWebEnginePage *self,
    const QString *text,
    QFlags<QWebEnginePage::FindFlag> flags,
    const void *callback
) asm(
    "_ZN14QWebEnginePage8findTextERK7QString6QFlagsINS_8FindFlagEERKSt8functionIFvRK24QWebEngineFindTextResultEE"
);

extern "C" void torrhunt_find_text(
    QWebEnginePage *self,
    const QString *text,
    QFlags<QWebEnginePage::FindFlag> flags,
    const void *callback
) {
    FunctionWrapper<FindTextInvoker, const QWebEngineFindTextResult &> fn(
        callback
    );
    std::function<void(const QWebEngineFindTextResult &)> f(std::move(fn));
    self->findText(*text, flags, f);
}

extern "C" void torrhunt_run_javascript(
    QWebEnginePage *self,
    const QString *script,
    const void *callback
) asm(
    "_ZN14QWebEnginePage13runJavaScriptERK7QStringRKSt8functionIFvRK8QVariantEE"
);

extern "C" void torrhunt_run_javascript(
    QWebEnginePage *self,
    const QString *script,
    const void *callback
) {
    FunctionWrapper<VariantInvoker, const QVariant &> fn(callback);
    self->runJavaScript(*script, std::move(fn));
}

extern "C" void torrhunt_run_javascript_world(
    QWebEnginePage *self,
    const QString *script,
    quint32 worldId,
    const void *callback
) asm(
    "_ZN14QWebEnginePage13runJavaScriptERK7QStringjRKSt8functionIFvRK8QVariantEE"
);

extern "C" void torrhunt_run_javascript_world(
    QWebEnginePage *self,
    const QString *script,
    quint32 worldId,
    const void *callback
) {
    FunctionWrapper<VariantInvoker, const QVariant &> fn(callback);
    self->runJavaScript(*script, worldId, std::move(fn));
}

extern "C" void torrhunt_single_shot(
    std::chrono::nanoseconds interval,
    Qt::TimerType timerType,
    const QObject *receiver,
    QtPrivate::QSlotObjectBase *slotObj
) asm(
    "_ZN6QTimer14singleShotImplENSt6chrono8durationIlSt5ratioILl1ELl1000000000EEEEN2Qt9TimerTypeEPK7QObjectPN9QtPrivate15QSlotObjectBaseE"
);

// singleShotImpl is private, so call the libc++-mangled symbol directly.
extern "C" void qt_single_shot_impl(
    std::chrono::nanoseconds interval,
    Qt::TimerType timerType,
    const QObject *receiver,
    QtPrivate::QSlotObjectBase *slotObj
) asm(
    "_ZN6QTimer14singleShotImplENSt3__16chrono8durationIxNS0_5ratioILl1ELl1000000000EEEEEN2Qt9TimerTypeEPK7QObjectPN9QtPrivate15QSlotObjectBaseE"
);

extern "C" void torrhunt_single_shot(
    std::chrono::nanoseconds interval,
    Qt::TimerType timerType,
    const QObject *receiver,
    QtPrivate::QSlotObjectBase *slotObj
) {
    qt_single_shot_impl(interval, timerType, receiver, slotObj);
}

extern "C" bool torrhunt_mkpath(
    const QDir *self,
    const QString *path,
    std::optional<QFlags<QFileDevice::Permission>> permissions
) asm(
    "_ZNK4QDir6mkpathERK7QStringSt8optionalI6QFlagsIN11QFileDevice10PermissionEEE"
);

extern "C" bool torrhunt_mkpath(
    const QDir *self,
    const QString *path,
    std::optional<QFlags<QFileDevice::Permission>> permissions
) {
    return self->mkpath(*path, permissions);
}
