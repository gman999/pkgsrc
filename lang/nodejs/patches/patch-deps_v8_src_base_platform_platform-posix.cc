$NetBSD: patch-deps_v8_src_base_platform_platform-posix.cc,v 1.2 2015/08/26 06:57:01 rumko Exp $

Use sysconf(_SC_THREAD_STACK_MIN) instead of PTHREAD_STACK_MIN.
Cast explicitly.

--- deps/v8/src/base/platform/platform-posix.cc.orig	2015-03-31 22:13:01.000000000 +0000
+++ deps/v8/src/base/platform/platform-posix.cc
@@ -327,6 +327,8 @@ int OS::GetCurrentThreadId() {
   return static_cast<int>(syscall(__NR_gettid));
 #elif V8_OS_ANDROID
   return static_cast<int>(gettid());
+#elif V8_OS_NETBSD || V8_OS_FREEBSD
+  return static_cast<int>(reinterpret_cast<intptr_t>(pthread_self()));
 #else
   return static_cast<int>(pthread_self());
 #endif
@@ -519,8 +521,13 @@ Thread::Thread(const Options& options)
     : data_(new PlatformData),
       stack_size_(options.stack_size()),
       start_semaphore_(NULL) {
+#if defined(__NetBSD__)
+  if (stack_size_ > 0 && static_cast<size_t>(stack_size_) < sysconf(_SC_THREAD_STACK_MIN)) {
+    stack_size_ = sysconf(_SC_THREAD_STACK_MIN);
+#else
   if (stack_size_ > 0 && static_cast<size_t>(stack_size_) < PTHREAD_STACK_MIN) {
     stack_size_ = PTHREAD_STACK_MIN;
+#endif
   }
   set_name(options.name());
 }
@@ -536,7 +543,7 @@ static void SetThreadName(const char* na
   pthread_set_name_np(pthread_self(), name);
 #elif V8_OS_NETBSD
   STATIC_ASSERT(Thread::kMaxThreadNameLength <= PTHREAD_MAX_NAMELEN_NP);
-  pthread_setname_np(pthread_self(), "%s", name);
+  pthread_setname_np(pthread_self(), "%s", (void *)name);
 #elif V8_OS_MACOSX
   // pthread_setname_np is only available in 10.6 or later, so test
   // for it at runtime.
