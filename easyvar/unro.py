"""A module that defines different undead and readonly classes.

Undead classes have non deletable attributes. Unro classes are
both non deletable and readonly.

-------------------------------------------------------------------
Copyright: Md. Jahidul Hamid <jahidulhamid@yahoo.com>

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
-------------------------------------------------------------------
"""





class Object(object):
    """Base class for all."""
    pass

class Base(Object):
    """A class that saves attributes and lets you iter through them
    """

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    __hash__ = Object.__hash__


class Map(Base):
    """A map interface that stores items as attributes.
    
    It provides iter through keys. Values can be accessed as items or attributes.
    """

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            for k, v in dict(*args, **kwargs).items():
                self[k] = v

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        super(Map, self).__setattr__(key, value)

    def __delitem__(self, key):
        super(Map, self).__delattr__(key)


####################################################################
##################### Some meta classes ############################
####################################################################

class UndeadMeta(type):
    """Metaclass that makes class attributes undead (not deletable)"""
    
    def __delattr__(self, name):
        raise AttributeError("type(%r) does not support attribute deletion." % (self))


class ReadonlyMeta(type):
    """Metaclass that makes class attributes readonly"""

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("type(%r) allows setting one attribute just once." % (self))
        else:
            super(ReadonlyMeta, self).__setattr__(name, value)

class UnroMeta(UndeadMeta, ReadonlyMeta):
    """Metaclass that makes attributes undead (not deletable) and readonly
    """
    pass

####################################################################


#####################################################################
################# Some class readonly attr storage class ############
#####################################################################


class ClassReadonlyMap(Map, metaclass=ReadonlyMeta):
    """An attribute mapping class that lets you set one class attribute just once.

    Once set, it can not be reset (unless deleted).

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassReadonly(Base, metaclass=ReadonlyMeta):
    """An attribute saving class that lets you set one class attribute just once.

    Once set, it can not be reset (unless deleted).

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassUndeadMap(Map, metaclass=UndeadMeta):
    """An attribute mapping class that lets you make undead class attributes that can not be killed.

    Once set, it can not be deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassUndead(Base, metaclass=UndeadMeta):
    """An attribute saving class that lets you make undead class attributes that can not be killed.

    Once set, it can not be deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassUnro(Base, metaclass=UnroMeta):
    """An attribute saving class that lets you make unro (undead + readonly)
    class attributes that can not be killed.

    Once set, it can not be reset or deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassUnroMap(Map, metaclass=UnroMeta):
    """An attribute mapping class that lets you make unro (undead and readonly)
    class attributes that can not be killed.

    Once set, it can not be reset or deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


#####################################################################


#####################################################################
### Some attribute storage class that impose same restrictions ######
### upon both class attributes and instance attributes ##############
#####################################################################

class ReadonlyMap(Map, metaclass=ReadonlyMeta):
    """An attribute mapping class that lets you set one item/attribute just once.

    Once set, it can not be reset (unless deleted).

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute/item just once." % (self.__class__))
        else:
            super(ReadonlyMap, self).__setattr__(name, value)


class Readonly(Base, metaclass=ReadonlyMeta):
    """An attribute saving class that lets you set one attribute just once.

    Once set, it can not be reset (unless deleted).

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once." % (self.__class__))
        else:
            super(Readonly, self).__setattr__(name, value)


class UndeadMap(Map, metaclass=UndeadMeta):
    """An attribute mapping class that lets you make undead attributes that can not be killed.

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class Undead(Base, metaclass=UndeadMeta):
    """An attribute saving class that lets you make undead attributes that can not be killed.

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class Unro(Base, metaclass=UnroMeta):
    """An attribute saving class that lets you set one attribute just once.

    Once set, it can not be reset or deleted.

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once." % (self.__class__))
        else:
            super(Unro, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class UnroMap(Map, metaclass=UnroMeta):
    """An attribute mapping class that lets you set one attribute just once.

    Once set, it can not be reset or deleted.

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once." % (self.__class__))
        else:
            super(UnroMap, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


####################################################################################################
######## Some more specialized class ###############################################################
####################################################################################################

class ConstClass(ClassUnro):
    """An attribute saving class that lets you set one attribute just the first time through class object.

    Instance object can not set any attributes.
    
    After setting the attribute, it becomes constant; neither can you reset it nor can you delete it.
    """
    
    def __setattr__(self, name, value):
        raise AttributeError("%r does not allow setting attributes through instance objects." % (self.__class__))

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))

####################################################################################################