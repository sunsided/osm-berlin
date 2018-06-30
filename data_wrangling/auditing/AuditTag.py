from xml.etree.cElementTree import Element
from typing import Tuple, Optional, Callable, Union, Iterable


class AuditTag:
    """
    Performs auditing of a single XML tag.
    """
    def __init__(self, applies_to_tag: Union[str, Iterable[str]],
                 filter_fn: Callable[[Element], bool],
                 audit_fn: Callable[[str], Tuple[bool, str]]):
        """
        Initializes a tag audit instance.
        :param applies_to_tag: The tag to which to apply the audit.
        :param filter_fn: A function that returns True if the audit step can be applied.
        :param audit_fn: A function returning either the original or corrected XML element or None
                         if the element could not be corrected.
        """
        if isinstance(applies_to_tag, str):
            applies_to_tag = {applies_to_tag}
        self._tag = set(applies_to_tag)
        self._filter = filter_fn
        self._audit = audit_fn
        self._attributes_removed = 0
        self._attributes_corrected = 0

    @property
    def attributes_removed(self) -> int:
        return self._attributes_removed

    @property
    def attributes_corrected(self) -> int:
        return self._attributes_corrected

    def audit(self, el: Element) -> Optional[Element]:
        """
        Audits the XML element.
        :param el: The element to audit.
        :return: An Element if no audit needed to be performed or was performed
                 automatically or None, if the element was invalid and could
                 not be corrected automatically.
        """
        if el.tag not in self._tag:
            return el
        for tag in list(el.iter('tag')):
            if not self._filter(tag):
                continue
            try:
                was_valid, corrected = self._audit(tag.attrib['v'])
                if was_valid:
                    continue
                if corrected is None:
                    el.remove(tag)
                    self._attributes_removed += 1
                    continue
                self._attributes_corrected += 1
                tag.attrib['v'] = corrected
            except ValueError:
                el.remove(tag)
                self._attributes_removed += 1
        return el

    def __call__(self, el: Element) -> Optional[Element]:
        """
        Audits the XML element.
        :param el: The element to audit.
        :return: An Element if no audit needed to be performed or was performed
                 automatically or None, if the element was invalid and could
                 not be corrected automatically.
        """
        return self.audit(el)

    def __repr__(self):
        return f'{type(self).__name__}: corrected {self.attributes_corrected}, removed {self.attributes_removed}'
