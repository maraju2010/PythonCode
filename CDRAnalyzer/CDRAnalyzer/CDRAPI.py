"""
This is an API module.User calls cdrapi class to run 2 loops in asyncronous mode.
    loop 1
        monitor.worker class - This will read cdr files from folder
    loop 2
        logic.algo class - This will read from sql db and anaylse and report
        suspicious authcodes.


"""

import sys
sys.path.append('C:/Users/manoraju/Desktop/pythonweb-app/pythonconfigure-karthik/CPO/updated/')
import threading
from CDRAnalyzer.monitor import worker,pool
from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.logic import algo_1 as algo
import asyncio

class cdrapi(object):

    async def _load_data(self):
        self.w=worker.Worker()
        self._p= worker._parser()
        fl=self.w._start()
        async for f in fl:
            self._p._parse(fp=f,tb="cdr_main",db="cdr_portal")

    async def _read_data(self):
        self.a=algo.auth_code_sn()
        await self.a._analyse()


if __name__ == '__main__':
    c = cdrapi()
    tasks = [
        asyncio.ensure_future(c._load_data()),
        asyncio.ensure_future(c._read_data())
    ]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except:
        """ write to recovery table and cache if an exception is raised"""
        c.a.recovery_close()
        c.w.write_to_cache()
    loop.close()
