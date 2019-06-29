import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Actor, Movie


# Graphql Type for Actor
class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


# Graphql Type for Movie
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


# The query type
class Query(ObjectType):
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)

    def resolve_actor(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Actor.objects.get(pk=id)

        return None

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Movie.objects.get(pk=id)

        return None

    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()


# Define Input object for mutations
# They should be defined baseo on the registered types

class ActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class MovieInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()


# Defining mutations
class CreateActor(graphene.Mutation):
    class Arguments:
        actor_data = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, actor_data=None):
        ok = True
        actor_instance = Actor(name=actor_data.name)
        actor_instance.save()
        return CreateActor(ok=ok, actor=actor_instance)


class UpdateActor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        actor_data = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, actor_data=None):
        ok = False
        actor_instance = Actor.objects.get(pk=id)

        if actor_instance:
            ok = True
            actor_instance.name = actor_data.name
            actor_instance.save()
            return UpdateActor(ok=ok, actor=actor_instance)

        return UpdateActor(ok=ok, actor=None)


class CreateMovie(graphene.Mutation):
    class Arguments:
        movie_data = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, movie_data=None):
        ok = True
        actors = []

        for actor in movie_data.actors:
            actor_instance = Actor.objects.get(pk=actor.id)

            if actor_instance is None:
                return CreateMovie(ok=False, movie=None)

            actors.append(actor_instance)

        movie_instance = Movie(title=movie_data.title, year=movie_data.year)
        movie_instance.save()
        movie_instance.actors.set(actors)
        return CreateActor(ok=ok, movie=movie_instance)


class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        data = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, data=None):
        ok = False
        movie_instance = Movie.objects.get(pk=id)
        print(movie_instance)

        if movie_instance:
            ok = True
            actors = []
            for actor in data.actors:
                actor_instance = Actor.objects.get(pk=actor.id)

                if actor_instance is None:
                    return UpdateMovie(ok=False, movie=None)

                actors.append(actor_instance)

            movie_instance.title = data.title
            movie_instance.year = data.year
            movie_instance.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(ok=ok, movie=movie_instance)

        return UpdateActor(ok=ok, movie=None)


class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
