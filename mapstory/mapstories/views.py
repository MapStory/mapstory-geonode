import json
import requests

from django.http import HttpResponse

from .models import Map
from .models import MapStory
from .models import StoryPin
from geonode.people.models import Profile


def save_mapstory(request):
    config = json.loads(request.body)
    print config

    if config['storyID']:
        mapstory = MapStory.objects.get(pk=config['storyID'])
        print("Found a mapstory, it is", mapstory)
    else:
        mapstory = MapStory(owner=request.user)
        print("There was no MapStory, making a new one.", mapstory)

    mapstory.save()
    config['storyID'] = mapstory.id
    mapstory.update_from_viewer(conf=config)

    for index, chapter in enumerate(config['chapters']):

        config['chapters'][index]['storyID'] = mapstory.id

        if config['chapters'][index]['mapId']:
            currentChapter = Map.objects.get(pk=config['chapters'][index]['mapId'])
        else:
            currentChapter = Map(owner=request.user, zoom=0, center_x=0, center_y=0)

        currentChapter.save()
        currentChapter.update_from_viewer(conf=chapter)
        config['chapters'][index]['mapId'] = currentChapter.id

        if chapter['pins']['features']:
            for index, pin in enumerate(chapter['pins']['features']):
                print(pin)
                if pin['id']:
                    currentPin = StoryPin.objects.get(pk=pin['id'])
                else:
                    print("PIN ID IS NULL")
                    currentPin = StoryPin()

                currentPin.map_id = chapter['mapId']

                #currentPin.auto_show = pin['properties']['autoShow']
                currentPin.content = pin['properties']['content']
                #currentPin.end_time = pin['properties']['end_time']
                currentPin.in_map = pin['properties']['inMap']
                currentPin.in_timeline = pin['properties']['inTimeline']
                currentPin.media = pin['properties']['media']
                #currentPin.start_time = pin['properties']['start_time']
                currentPin.title = pin['properties']['title']

                currentPin.save()
                pin['id'] = currentPin.id

    return HttpResponse(json.dumps(config))


