from pytest_factoryboy import register
from tests.accounts_factories import (
    AccountFactory,
    TicketFactory,
    TicketAnswerFactory,
    CouponFactory,
    ShoppingCartFactory,
    CartItemFactory,
)
from tests.blog_factories import (
    BlogCategoryFactory,
    TagFactory,
    PostFactory,
    CommentFactory,
)
from tests.products_factories import (
    CategoryFactory,
    BrandFactory,
    ProductTypeFactory,
    ProductSpecificationFactory,
    ProductSpecificationValueFactory,
    ProductFactory,
    ProductCommentFactory,
)

# <<< =================== Accounts =================== >>>
register(AccountFactory)
register(TicketFactory)
register(TicketAnswerFactory)
register(CouponFactory)
register(ShoppingCartFactory)
register(CartItemFactory)

# <<< =================== Products =================== >>>
register(BlogCategoryFactory)
register(TagFactory)
register(PostFactory)
register(CommentFactory)

# <<< =================== Blog =================== >>>
register(CategoryFactory)
register(BrandFactory)
register(ProductTypeFactory)
register(ProductSpecificationFactory)
register(ProductSpecificationValueFactory)
register(ProductFactory)
register(ProductCommentFactory)
