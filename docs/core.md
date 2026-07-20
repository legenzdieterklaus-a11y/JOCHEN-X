# Core

The core is composed exclusively by `ApplicationHost`. `ServiceRegistry` supports singleton,
transient, scoped, typed, and factory registrations. Resolution is lazy and validates dependency
graphs with circular-dependency detection. `LifecycleManager` owns ordered start, stop, restart,
recovery, and health state without starting threads itself.
