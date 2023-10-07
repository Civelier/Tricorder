import sys
from typing import Any, Callable, Dict, Generic, Iterable, Iterator, MutableSequence, TypeVar, Union, overload, SupportsIndex
from mvvm.common import BaseType, Event, EventArgs
from mvvm.models.model import *

_T = TypeVar("_T", int, str, float, bool)
_TT = TypeVar("_TT", int, str, float, bool)

class ItemAddedEventArgs(EventArgs, Generic[_T]):
    def __init__(self, index: SupportsIndex, value:_T):
        self.index = index
        self.value = value
        
class ItemRemovedEventArgs(EventArgs, Generic[_T]):
    def __init__(self, index: SupportsIndex, value:_T):
        self.index = index
        self.value = value
        
class ItemChangedEventArgs(EventArgs, Generic[_T]):
    def __init__(self, index: SupportsIndex, oldVal:_T, newVal:_T):
        self.index = index
        self.oldVal = oldVal
        self.newVal = newVal

class ListModel(ModelBase, MutableSequence[_T], Generic[_T]):
    @overload
    def __init__(self):
        Model.__init__(self)
        self._list = list()
        self.itemAdded:Event[ListModel[_T], ItemAddedEventArgs[_T]] = Event()
        self.itemRemoved:Event[ListModel[_T], ItemRemovedEventArgs[_T]] = Event()
        self.itemChanged:Event(ListModel[_T], ModelUpdatedEventArgs) = Event()
        
    @overload
    def __init__(self, __iterable: Iterable[_T]):
        Model.__init__(self)
        self._list = list(__iterable)
        self.itemAdded:Event[ListModel[_T], ItemAddedEventArgs[_T]] = Event()
        self.itemRemoved:Event[ListModel[_T], ItemRemovedEventArgs[_T]] = Event()
        self.itemChanged:Event(ListModel[_T], ModelUpdatedEventArgs) = Event()
    
    def on_item_added(self, index:SupportsIndex, value:_T):
        self.itemAdded(self, ItemAddedEventArgs(index, value))
        self.updated(self, ModelUpdatedEventArgs())

    def on_item_removed(self, index:SupportsIndex, value:_T):
        self.itemRemoved(self, ItemRemovedEventArgs(index, value))
        self.updated(self, ModelUpdatedEventArgs())

    def on_item_changed(self, index:SupportsIndex, oldVal:_T, newVal:_T):
        self.itemChanged(self, ItemChangedEventArgs(index, oldVal, newVal))
        self.updated(self, ModelUpdatedEventArgs())
    
    def copy(self):
        return ListModel(self._list.copy())
    def append(self, __object: _T):
        self._list.append(__object)
        if isinstance(__object, ModelBase):
            __object.updated += self.updated
        self.on_item_added(len(self._list)-1, __object)
    def extend(self, __iterable: Iterable[_T]) -> None:
        pass
    def pop(self, __index: SupportsIndex = -1) -> _T:
        p = self._list.pop(__index)
        if isinstance(p, ModelBase):
            p.updated -= self.updated
        self.on_item_removed(__index, p)
        return p
        
    # Signature of `list.index` should be kept in line with `collections.UserList.index()`
    # and multiprocessing.managers.ListProxy.index()
    def index(self, __value: _T, __start: SupportsIndex = 0, __stop: SupportsIndex = sys.maxsize) -> int: 
        return self._list.index(__value, __start, __stop)
    
    def count(self, __value: _T) -> int:
        return self._list.count(__value)
    
    def insert(self, __index: SupportsIndex, __object: _T) -> None:
        if isinstance(__object, ModelBase):
            __object.updated += self.updated
        self._list.insert(__index, __object)
        self.on_item_added(__index, __object)
        
    def remove(self, __value: _T) -> None:
        try:
            i = self._list.index(__value)
        except ValueError:
            return None
        self._list.remove(__value)
        if isinstance(__value, ModelBase):
            __value.updated -= self.updated
        self.on_item_removed(i, __value)
    # Signature of `list.sort` should be kept inline with `collections.UserList.sort()`
    # and multiprocessing.managers.ListProxy.sort()
    #
    # Use list[SupportsRichComparisonT] for the first overload rather than [SupportsRichComparison]
    # to work around invariance
    @overload
    def sort(self, *, key: None = None, reverse: bool = False) -> None:
        pass
    @overload
    def sort(self, *, key: Callable[[_T], Any], reverse: bool = False) -> None:
        pass
    def __len__(self) -> int:
        return self._list.__len__()
    def __iter__(self) -> Iterator[_T]:
        return self._list.__iter__()
    @overload
    def __getitem__(self, __i: SupportsIndex) -> _T:
        return self._list.__getitem__(__i)
    @overload
    def __getitem__(self, __s: slice):
        pass
    @overload
    def __setitem__(self, __key: SupportsIndex, __value: _T) -> None:
        old = self._list.__getitem__(__key)
        if old != __value:
            self._list(__key, __value)
            self.on_item_changed(__key, old, __value)
    @overload
    def __setitem__(self, __key: slice, __value: Iterable[_T]) -> None:
        pass
    def __delitem__(self, __key: Union[SupportsIndex, slice]) -> None:
        pass
    def __contains__(self, __key: object) -> bool:
        return self._list.__contains__(__key)
    def __reversed__(self) -> Iterator[_T]:
        pass