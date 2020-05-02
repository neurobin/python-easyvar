"""Deprecators

"""

__author__ = 'Md Jahidul Hamid <jahidulhamid@yahoo.com>'
__copyright__ = 'Copyright © Md Jahidul Hamid <https://github.com/neurobin/>'
__license__ = '[BSD](http://www.opensource.org/licenses/bsd-license.php)'
__version__ = '0.0.1'


import inspect
import traceback
import warnings
import functools
from packaging import version

from easyvar.warnings import UnsupportedWarning
from easyvar.warnings import DeprecatedWarning


class DepWrapper(object):
    STATUS_OK = 0
    STATUS_DEPRECATED = 1
    STATUS_UNSUPPORTED = 2

    def __init__(self, func,
                me='',
                by='',
                ver_cur='',
                ver_dep='',
                ver_end='',
                msg_dep='',
                msg_end='',
                do_at_dep='',
                do_at_end='',
                stacklevel=2):
        self.func_callable = True
        if not callable(func):
            self.func_callable = False
            if not me:
                raise ValueError("If a non-callable is being deprecated, you "
                                 "must pass the name of the object using the "
                                 "'me' parameter to the deprecate call.")
        self.me = me if me else repr(func) # guarded by above raise
        self.func = func
        self.by = by
        self.ver_cur = ver_cur
        self.ver_dep = ver_dep
        self.ver_end = ver_end
        self.msg_dep = msg_dep
        self.msg_end = msg_end
        self.do_at_dep = do_at_dep
        self.do_at_end = do_at_end
        self.stacklevel = stacklevel
        (_ver_cur,
        _ver_dep,
        _ver_end) = (version.parse(x)
                        if x and isinstance(x, str)
                        else x
                        for x in (ver_cur, ver_dep, ver_end))
        self.status = self.STATUS_OK
        if _ver_end and _ver_cur >= _ver_end:
            self.status = self.STATUS_UNSUPPORTED
        elif _ver_cur >= _ver_dep:
            self.status = self.STATUS_DEPRECATED

    def get_deprecation_warning_config(self):
        # only called when status is not OK
        # thus this check is redundant
        # if self.status == self.STATUS_OK:
        #     return ''
        if self.by:
            self.by = " by `%s`" % (self.by,)
        if self.ver_dep:
            self.ver_dep = " from version `%s`" % (self.ver_dep,)
        if self.ver_cur:
            self.ver_cur = ". Current version `%s`" % (self.ver_cur,)
        if self.status == self.STATUS_UNSUPPORTED:
            self.me = "`%s` was deprecated" % (self.me,)
            if self.ver_end:
                self.ver_end = " and planned to be removed in version"\
                                   " `%s`" % (self.ver_end,)
            msg = ''.join((self.me, self.by, self.ver_dep, self.ver_end,
                                                         self.ver_cur))
            return UnsupportedWarning(msg), self.do_at_end
        else:
            self.me = "`%s` is deprecated" % (self.me,)
            if self.ver_end:
                self.ver_end = " and will be removed in version `%s`"\
                                % (self.ver_end,)

        msg = ''.join((self.me, self.by, self.ver_dep, self.ver_end,
                                                         self.ver_cur))
        return DeprecatedWarning(msg), self.do_at_dep

    def get_deprecation_function(self):
        if self.status == self.STATUS_OK:
            return self.func # no decoration
        # decoration needs to be done
        # get the message
        wrn, filter_wrn = self.get_deprecation_warning_config()
        @functools.wraps(self.func)
        def wrapper(*args, **kwargs):
            if filter_wrn:
                warnings.simplefilter(filter_wrn, wrn.__class__)
            warnings.warn(wrn,
                        # category=wrn.__class__, # category is ignored
                        # when message is a Warning instance
                        # category is set to wrn.__class__ by default
                        stacklevel=self.stacklevel)
            return self.func(*args, **kwargs)
        return wrapper

    def get_deprecation_wrapper(self):
        if self.func_callable:
            return self.get_deprecation_function()
        else:
            raise NotImplementedError("decorating a non callable is not"
                                        " supported yet.")

    def get_wrapper(self):
        return self.get_deprecation_wrapper()





def deprecate(_func=None, *,
              me='',
              by='',
              ver_cur='',
              ver_dep='',
              ver_end='',
              msg_dep='',
              msg_end='',
              do_at_dep='',
              do_at_end='',
              stacklevel=2,
              ):
    def deprecator(func):
        wrapper = DepWrapper(func, me=me, by=by,ver_cur=ver_cur,
                            ver_dep=ver_dep, ver_end=ver_end, msg_dep=msg_dep,
                            msg_end=msg_end, do_at_dep=do_at_dep,
                            do_at_end=do_at_end, stacklevel=stacklevel)
        return wrapper.get_wrapper()
    if _func:
        return deprecator(_func)
    return deprecator

def raiseUnsupportedWarning(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('error', UnsupportedWarning)
            try:
                result = func(*args, **kwargs)
            except:
                raise
        return result
    return wrapper
