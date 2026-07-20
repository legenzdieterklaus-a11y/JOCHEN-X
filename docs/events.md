# Events

`EventBus` supports synchronous and asynchronous publishing, priority-ordered subscriptions,
filters, glob-style event names, bounded history, and sticky events. It is thread safe. UI callers
must use `publish_async` for any handler that can block; synchronous publication is intentionally
reserved for brief in-process notifications.
