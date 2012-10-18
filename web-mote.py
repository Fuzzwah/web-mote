import web, os, json, random
import util, conf, player 

urls = (
    '/show-directory', 'showDirectory',
    '/play', 'play',
    '/command', 'command',
    '.*', 'index'
)

app = web.application(urls, globals())
        
class showDirectory:
    def POST(self):
        i = web.input()
        if i == {} or i['dir'] == "root":
            return util.entriesToJSON(conf.root)
        else: 
            assert util.isInRoot(i['dir'])
            return util.dirToJSON(i['dir'])

class play:
    def POST(self):
        t = web.input()['target']
        if os.path.isfile(t):
            fileQueue = [t]
        elif os.path.isdir(t):
            fileQueue = util.deepListDir(t)
        else:
            fileQueue = json.loads(t)
        if web.input().get('shuffle', False):
            random.shuffle(fileQueue)
        player.play(fileQueue)
        return util.entriesToJSON(fileQueue)

class command:
    def POST(self):
        assert player.activePlayer and web.input()['command']
        web.debug(web.input()['command'])
        player.commandQueue.put(web.input()['command'])

class index:
    def GET(self):
        raise web.seeother("/static/web-mote.html")

if __name__ == "__main__":
    app.run()
