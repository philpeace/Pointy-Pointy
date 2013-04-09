def add_routes(map):
    map.connect('home', '/', controller='controllers.Home:Home', action='index')
    map.connect('maplist', '/map', controller='controllers.Map:Map', action='list')
    map.connect('mapcreate', '/map/create', controller='controllers.Map:Map', action='create', conditions=dict(method=["POST"]))
    map.connect('mapnew', '/map/new', controller='controllers.Map:Map', action='new', conditions=dict(method=["GET"]))
    map.connect('map', '/map/{id}', controller='controllers.Map:Map', action='view')
    map.connect('mapedit', '/map/{id}/edit', controller='controllers.Map:Map', action='edit', conditions=dict(method=["GET"]))
    map.connect('mapupdate', '/map/{id}/edit', controller='controllers.Map:Map', action='update', conditions=dict(method=["POST"]))
    map.connect('default', '/{controller}/{action}/{id}')
