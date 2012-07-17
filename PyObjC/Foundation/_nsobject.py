"""
Define a category on NSObject with some useful methods.

FIXME: 
- add signature information (namedselector) to all methods
  (not strictly needed)
- add docstrings everywhere
- create unittests
"""
import objc 
import sys

NSObject = objc.lookUpClass('NSObject')

class NSObject (objc.Category(NSObject)):

    @objc.namedselector("_pyobjc_performOnThread:")
    def _pyobjc_performOnThread_(self, callinfo):
        try:
            sel, arg = callinfo
            m = self.methodForSelector_(sel)
            m(arg)
        except:
            import traceback
            traceback.print_exc(fp=sys.stderr)

    @objc.namedselector("_pyobjc_performOnThreadWithResult:")
    def _pyobjc_performOnThreadWithResult_(self, callinfo):
        try:
            sel, arg, result = callinfo
            m = self.methodForSelector_(sel)
            r = m(arg)
            result.append((True, r))
        except:
            result.append((False, sys.exc_info()))


    if hasattr(NSObject, "performSelector_onThread_withObject_waitUntilDone_"):
        @objc.namedselector("pyobjc_performSelector:onThread:withObject:waitUntilDone:")
        def pyobjc_performSelector_onThread_withObject_waitUntilDone_(
                self, aSelector, thread, arg, wait):
            """
            A version of performSelector:onThread:withObject:waitUntilDone: that
            will log exceptions in the called method (instead of aborting the
            NSRunLoop on the other thread).
            """
            self.performSelector_onThread_withObject_waitUntilDone_(
                    'pyobjc_performOnThread:', thread, (aSelector, arg), wait)

        @objc.namedselector("pyobjc_performSelector:onThread:withObject:waitUntilDone:modes:")
        def pyobjc_performSelector_onThread_withObject_waitUntilDone_modes_(
                self, aSelector, thread, arg, wait, modes):
            """
            A version of performSelector:onThread:withObject:waitUntilDone:modes: 
            that will log exceptions in the called method (instead of aborting the
            NSRunLoop on the other thread).
            """
            self.performSelector_onThread_withObject_waitUntilDone_modes_(
                'pyobjc_performOnThread:', thread, (aSelector, arg), wait, modes)

    @objc.namedselector("pyobjc_performSelector:withObject:afterDelay:")
    def pyobjc_performSelector_withObject_afterDelay_(
            self, aSelector, arg, delay):
        """
        A version of performSelector:withObject:afterDelay: 
        that will log exceptions in the called method (instead of aborting the
        NSRunLoop).
        """
        self.performSelector_withObject_afterDelay_(
            'pyobjc_performOnThread:', (aSelector, arg), delay)

    @objc.namedselector("pyobjc_performSelector:withObject:afterDelay:inModes:")
    def pyobjc_performSelector_withObject_afterDelay_inModes_(
            self, aSelector, arg, delay, modes):
        """
        A version of performSelector:withObject:afterDelay:inModes:
        that will log exceptions in the called method (instead of aborting the
        NSRunLoop).
        """
        self.performSelector_withObject_afterDelay_inModes_(
            'pyobjc_performOnThread:', (aSelector, arg), delay, modes)

    if hasattr(NSObject, "performSelectorInBackground_withObject_waitUntilDone_"):
        @objc.namedselector("pyobjc_performSelectorInBackground:withObject:")
        def pyobjc_performSelectorInBackground_withObject_(
                self, aSelector, arg):
            """
            A version of performSelectorInBackground:withObject:
            that will log exceptions in the called method (instead of aborting the
            NSRunLoop).
            """
            self.performSelectorInBackground_withObject_(
                'pyobjc_performOnThread:', (aSelector, arg))


    @objc.namedselector("pyobjc_performSelectorInBackground:withObject:waitUntilDone:")
    def pyobjc_performSelectorOnMainThread_withObject_waitUntilDone_(
            self, aSelector, arg, wait):
        """
        A version of performSelectorOnMainThread:withObject:waitUntilDone:
        that will log exceptions in the called method (instead of aborting the
        NSRunLoop in the main thread).
        """
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            'pyobjc_performOnThread:', (aSelector, arg), wait)

    @objc.namedselector("pyobjc_performSelectorOnMainThread:withObject:waitUntilDone:modes:")
    def pyobjc_performSelectorOnMainThread_withObject_waitUntilDone_modes_(
            self, aSelector, arg, wait, modes):
        """
        A version of performSelectorOnMainThread:withObject:waitUntilDone:modes:
        that will log exceptions in the called method (instead of aborting the
        NSRunLoop in the main thread).
        """
        self.performSelectorOnMainThread_withObject_waitUntilDone_modes_(
            'pyobjc_performOnThread:', (aSelector, arg), wait, modes)


    # And some a some versions that return results

    @objc.namedselector("pyobjc_performSelectorOnMainThread:withObject:modes:")
    def pyobjc_performSelectorOnMainThread_withObject_modes_(
            self, aSelector, arg, modes):
        """
        Simular to performSelectorOnMainThread:withObject:waitUntilDone:modes:,
        but:

        - always waits until done
        - returns the return value of the called method
        - if the called method raises an exception, this will raise the same
           exception
        """
        result = []
        self.performSelectorOnMainThread_withObject_waitUntilDone_modes_(
            'pyobjc_performOnThreadWithResult:', 
            (aSelector, arg, result), True, modes)
        isOK, result = result[0]

        if isOK:
            return result
        else:
            exc_type, exc_value, exc_trace = result
            raise exc_type, exc_value, exc_trace

    @objc.namedselector("pyobjc_performSelectorOnMainThread:withObject:")
    def pyobjc_performSelectorOnMainThread_withObject_(
            self, aSelector, arg):
        result = []
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            'pyobjc_performOnThreadWithResult:', 
            (aSelector, arg, result), True)
        isOK, result = result[0]

        if isOK:
            return result
        else:
            exc_type, exc_value, exc_trace = result
            raise exc_type, exc_value, exc_trace

    if hasattr(NSObject, "performSelector_onThread_withObject_waitUntilDone_"):
        # These methods require Leopard, don't define them if the 
        # platform functionality isn't present.

        @objc.namedselector("pyobjc_performSelector:onThread:withObject:modes:")
        def pyobjc_performSelector_onThread_withObject_modes_(
                self, aSelector, thread, arg, modes):
            result = []
            self.performSelector_onThread_withObject_waitUntilDone_modes_(
                'pyobjc_performOnThreadWithResult:', thread,
                (aSelector, arg, result), True, modes)
            isOK, result = result[0]

            if isOK:
                return result
            else:
                exc_type, exc_value, exc_trace = result
                raise exc_type, exc_value, exc_trace

        @objc.namedselector("pyobjc_performSelector:onThread:withObject:")
        def pyobjc_performSelector_onThread_withObject_(
                self, aSelector, thread, arg):
            result = []
            self.performSelector_onThread_withObject_waitUntilDone_(
                'pyobjc_performOnThreadWithResult:', thread,
                (aSelector, arg, result), True)
            isOK, result = result[0]

            if isOK:
                return result
            else:
                exc_type, exc_value, exc_trace = result
                raise exc_type, exc_value, exc_trace


del NSObject
