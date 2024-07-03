from django.db.models import Avg
from django.contrib.auth.models import User
from product.models import ReviewModel
# Assuming Category, Brand, Activity are defined here
from home.models import Product


def get_rating_based_recommendations(user):
    # Fetch all reviews by the current user
    user_reviews = ReviewModel.objects.filter(user=user)

    # Get products rated highly by this user
    highly_rated_products = ReviewModel.objects.filter(
        user=user, rating__gte=4)

    # Get other users who have rated those highly rated products positively
    similar_users = set()
    for review in highly_rated_products:

        all_review_rated_highly = ReviewModel.objects.filter(
            product=review.product, rating__gte=4)
        for r in all_review_rated_highly:
            similar_users.add(r.user)
    similar_users.remove(user)

    # Get products that these similar users have rated highly
    recommended_products = Product.objects.filter(
        reviewmodel__user__in=similar_users
    ).annotate(
        avg_rating=Avg('reviewmodel__rating')
    ).order_by('-avg_rating')[:10]

    return recommended_products


# from django.db.models import Avg
# from home.models import Product
# from product.models import ReviewModel
# from django.contrib.auth.models import User


# def get_rating_based_recommendations(user):
#     # Fetch all reviews by the current user
#     user_reviews = ReviewModel.objects.filter(user=user)

#     # Get products rated highly by this user
#     highly_rated_products = ReviewModel.objects.filter(
#         user=user, rating__gte=4)

#     # Get other users who have rated those highly rated products positively
#     similar_users = User.objects.filter(
#         reviewmodel__in=highly_rated_products).exclude(id=user.id).distinct()

#     # Get products that these similar users have rated highly
#     recommended_products = Product.objects.filter(reviewmodel_userin=similar_users).annotate(
#         avg_rating=Avg('reviewmodel_rating')).order_by('-avg_rating')[:10]

#     return recommended_products
