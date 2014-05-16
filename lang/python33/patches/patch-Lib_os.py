$NetBSD: patch-Lib_os.py,v 1.1.2.2 2014/05/16 14:00:36 schnoebe Exp $

Fix CVE-2014-2667 based on upstream:
http://hg.python.org/cpython/rev/6370d44013f7

--- Lib/os.py.orig	2014-03-09 08:40:12.000000000 +0000
+++ Lib/os.py
@@ -230,23 +230,16 @@ SEEK_SET = 0
 SEEK_CUR = 1
 SEEK_END = 2
 
-
-def _get_masked_mode(mode):
-    mask = umask(0)
-    umask(mask)
-    return mode & ~mask
-
 # Super directory utilities.
 # (Inspired by Eric Raymond; the doc strings are mostly his)
 
 def makedirs(name, mode=0o777, exist_ok=False):
     """makedirs(path [, mode=0o777][, exist_ok=False])
 
-    Super-mkdir; create a leaf directory and all intermediate ones.
-    Works like mkdir, except that any intermediate path segment (not
-    just the rightmost) will be created if it does not exist. If the
-    target directory with the same mode as we specified already exists,
-    raises an OSError if exist_ok is False, otherwise no exception is
+    Super-mkdir; create a leaf directory and all intermediate ones.  Works like
+    mkdir, except that any intermediate path segment (not just the rightmost)
+    will be created if it does not exist. If the target directory already
+    exists, raise an OSError if exist_ok is False. Otherwise no exception is
     raised.  This is recursive.
 
     """
@@ -268,20 +261,7 @@ def makedirs(name, mode=0o777, exist_ok=
     try:
         mkdir(name, mode)
     except OSError as e:
-        dir_exists = path.isdir(name)
-        expected_mode = _get_masked_mode(mode)
-        if dir_exists:
-            # S_ISGID is automatically copied by the OS from parent to child
-            # directories on mkdir.  Don't consider it being set to be a mode
-            # mismatch as mkdir does not unset it when not specified in mode.
-            actual_mode = st.S_IMODE(lstat(name).st_mode) & ~st.S_ISGID
-        else:
-            actual_mode = -1
-        if not (e.errno == errno.EEXIST and exist_ok and dir_exists and
-                actual_mode == expected_mode):
-            if dir_exists and actual_mode != expected_mode:
-                e.strerror += ' (mode %o != expected mode %o)' % (
-                        actual_mode, expected_mode)
+        if not exist_ok or e.errno != errno.EEXIST or not path.isdir(name):
             raise
 
 def removedirs(name):
