# Performance

`PerformanceController` selects a policy mode: normal, gaming, idle, low-power, benchmark, sleep,
or maintenance. It does not alter hardware or spawn monitors. Resource collection is represented by
the synchronous `ResourceMonitor` port and immutable `ResourceSnapshot`.
