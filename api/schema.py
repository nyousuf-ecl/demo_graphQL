import graphene

from graphene_django.types import DjangoObjectType 

from .models import *


class LocationType(DjangoObjectType):
    class Meta: 
        model = Location

class EventType(DjangoObjectType):
    class Meta:
        model = Event

class AccountType(DjangoObjectType):
    class Meta: 
        model = Account

class Event_memberType(DjangoObjectType):
    class Meta: 
        model = Event_member


class Query(graphene.ObjectType):
    all_members = graphene.List(Event_memberType)

    event = graphene.List(EventType, name = graphene.String())

    location = graphene.List(LocationType, altitude = graphene.Float())

    event_member = graphene.List(Event_memberType, user_id=graphene.ID(), event_id=graphene.ID())

    def resolve_all_members(self, info, **kwargs):
        return Event_member.objects.all()
      
    def resolve_event(self, info, **kwargs):
      name = kwargs.get('name')

      if name is not None:
        return [Event.objects.get(name=name)]
      else:
        return Event.objects.all()

    def resolve_location(self, info, **kwargs):
      altitude = kwargs.get('altitude')
      if altitude is not None:
        return [Location.objects.get(altitude=altitude)]
      else:
        return Location.objects.all()

    def resolve_event_member(self, info, **kwargs):
      user_id = kwargs.get('user_id')
      event_id = kwargs.get('event_id')
      print(user_id)
      print(event_id)
      if user_id is not None:
        print(Event_member.objects.get(user_id = user_id))
        return [Event_member.objects.get(user_id = user_id)]
      if event_id is not None:
        return [Event_member.objects.get(event_id = event_id)]
      else:
        return Event_member.objects.all()


# "inputs"
class LocationInput(graphene.InputObjectType):
    id = graphene.ID()
    latitude = graphene.Float()
    altitude = graphene.Float()

class EventInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    location = graphene.InputField(LocationInput)


# class CreateLocation(graphene.Mutation):
#     class Arguments:
#         input = LocationInput(required=True)

#     location = graphene.Field(LocationType)

#     def mutate(self, info, input=None):
#         location_instance = Location(latitude=input.latitude, altitude=input.altitude)
#         location_instance.save()
        
#         return CreateLocation(location=location_instance)
  

class CreateEvent(graphene.Mutation):
    class Arguments:
        input = EventInput(required=True)
        
    event = graphene.Field(EventType)

    def mutate(self, info, input=None):
        # locations = []
        # for location_input in input.locations:
        #     location = Location.objects.get(pk=location_input.id)
        #     if location is None:
        #         return CreateEvent(event=None)
        #     locations.append(location)
        loc = input.get("location")
        # print(input.__dict__)
        # print(loc.__dict__)
        location = Location.objects.get(pk=loc.id)
        # print(location.__dict__)
        event_instance = Event(name=input.name, description=input.description)
        event_instance.location = location
        event_instance.save()
        

        return CreateEvent(event=event_instance)

class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = EventInput(required=True)

    event = graphene.Field(EventType)

    def mutate(self, info, id, input=None):
        event_instance = Event.objects.get(pk=id)
        loc = input.get("location")
        location = Location.objects.get(pk=loc.id)
        if event_instance:
            if event_instance.name is not None:
                event_instance.name = input.name
            if event_instance.description is not None:
                event_instance.description = input.description
            if event_instance.location is not None: 
                event_instance.location = location

            event_instance.save()
            
            return UpdateEvent(event=event_instance)

class DeleteEvent(graphene.Mutation):
  class Arguments:
    id = graphene.ID(required=True)
  
  event = graphene.Field(EventType)

  def mutate(self, info, id):
    event = Event.objects.get(pk=id)
    event.delete()

    return DeleteEvent(event=None)

# class EventCreateMutation(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#         description = graphene.String(required=True)
#         location_id = graphene.ID(required=True)

#     event = graphene.Field(EventType)

#     def mutate(self, info, name, description, location_id):
#         location = Location.objects.get(id=location_id)
#         event = Event.objects.create(name=name, description=description, location=location)

#         return EventCreateMutation(event=event)

# class EventUpdateMutation(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)
#         location_id = graphene.ID(required=True)
        
#     event = graphene.Field(EventType)

#     def mutate(self, info, id, location_id):
#         event = Event.objects.get(pk=id)
#         location = Location.objects.get(pk=location_id)

#         if location_id is not None:
#             event.location = location
        
#         event.save()

#         return EventUpdateMutation(event=event)


class Mutation:
    # create_location = CreateLocation.Field()
    create_event = CreateEvent.Field()  
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()
    # update_event  = EventCreateMutation.Field()
    # update_event  = EventUpdateMutation.Field()

""" 
query memberAll{
  allMembers{
   id
   userId{
     email
   }
   eventId{
     name
   }
  }
}

query singleEvent{
  event(name:"React Event"){
    id
    name
    description
    location{
      id
      latitude
      altitude
    }
  }
}

query allEvent{
  event{
    id
    name
    description
    location{
      id
      latitude
      altitude
    }
  }
}

query memberEventSearch{
 eventMember(userId:2){
  	id
  	userId{
      id
      email
    }
  	eventId{
      id
      name
    }
	}
}


query eventMemberSearch{
 eventMember(eventId:2){
  	id
  	userId{
      id
      email
    }
  	eventId{
      id
      name
    }
	}
}

mutation eventCreate{
  createEvent(input: {
    name: "Covid-19",
    description: "Session on Covid-19",
    location: {
      id: 1
    }
  })
  {
    event{
      id
      name
      description
      location{
        id
        latitude
        altitude
      }
    }
  }
}

mutation eventUpdate{
  updateEvent(id:22, input:{
    name: "Vue Js Event",
    description: "Session on Vue Js"
    location: {
      id: 2
    }
  }){
     event{
      id
      name
      description
      location{
        id
        latitude
        altitude
      }
    }
  }
}

mutation eventDelete{
  deleteEvent(id: 23){
    event{
      id
    }
  }
}

"""