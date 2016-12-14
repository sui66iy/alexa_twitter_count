
from twitter_api import TwitterAPI

from fuzzywuzzy import (process, fuzz)

class Celebrinator(object):

    celebrities = {
        'donald trump': 'realDonaldTrump',
        'hillary clinton': 'HillaryClinton',
        'michael higgins': 'sui66iy',
        'kanye west': 'kanyewest'
        }

    def _get_match(self, celebrity):
        phrase = celebrity.strip().lower()
        best = process.extractOne(phrase, self.celebrities.keys(), scorer=fuzz.ratio)
        if best is None:
            return None
        (choice, score) = best
        if score < 50:
            return None
        return (choice, self.celebrities[choice])
            
    def followers(self, celebrity):
        match = self._get_match(celebrity)
        if match is None:
            raise ValueError(celebrity)
        (celebrity_name, celebrity_handle) = match
        tapi = TwitterAPI()
        follower_count = tapi.followers(celebrity_handle)

        return "%s has %d Twitter followers." % (celebrity_name.title(), follower_count)

        
    
    
