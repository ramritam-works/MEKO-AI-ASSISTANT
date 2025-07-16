from dotenv import load_dotenv
load_dotenv()
from kivy import app, clock
from meko import Meko

class MykivyApp(app.App):
    def build(self):
        meko = Meko()
        meko.start_listening()
        
        self.update_event = clock.Clock.schedule_interval(meko.update_circle,1/60)
        self.btn_rotation_event = clock.Clock.schedule_interval(meko.circle.rotate_button,1/60)
        
        return meko
    
    
if __name__ == '__main__':
    MykivyApp = MykivyApp()
    MykivyApp.run()    