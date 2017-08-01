"""
byceps.services.shop.article.models.compilation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from typing import Iterator, List, Optional

from .article import Article


class ArticleCompilationItem:

    def __init__(self, article: Article, *, fixed_quantity: Optional[int]=None
                ) -> None:
        if (fixed_quantity is not None) and fixed_quantity < 1:
            raise ValueError(
                'Fixed quantity, if given, must be a positive number.')

        self.article = article
        self.fixed_quantity = fixed_quantity

    def has_fixed_quantity(self) -> bool:
        return self.fixed_quantity is not None


class ArticleCompilation:

    def __init__(self) -> None:
        self._items = []  # type: List[ArticleCompilationItem]

    def append(self, item: ArticleCompilationItem) -> None:
        self._items.append(item)

    def __iter__(self) -> Iterator[ArticleCompilationItem]:
        return iter(self._items)

    def is_empty(self) -> bool:
        return not self._items
