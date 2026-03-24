from state.world_model import WorldModel
# from perception.mock_observer import MockObserver
from geometry.zones import PARKING_ZONES
from logic.occupancy_engine import OccupancyEngine
from debug.topdown_view import TopDownView
from replay.recorder import ObservationRecorder
from replay.player import ObservationPlayer
from debug.timeline import TimelineRecorder
from perception.camera_observer import CameraObserver
from debug.camera_view import CameraView
import cv2
import time

camera_view = CameraView()
viewer = TopDownView()
occupancy_engine = OccupancyEngine()
timeline = TimelineRecorder()

MODE = "record"
# MODE = "replay"

if MODE == "record":
    # observer = MockObserver()
    observer = CameraObserver()
    recorder = ObservationRecorder("observations.json")

elif MODE == "replay":
    observer = ObservationPlayer("observations.json")
    recorder = None

def main():
    world = WorldModel() # current belief of reality

    try:
        while True:
            observations, frame = observer.get_observations()
            dt = observer.dt

            if frame is None:
                break

            # check if entity is inside any parking zone
            occupancy = occupancy_engine.compute(world, PARKING_ZONES)

            if recorder is not None:
                recorder.record(observations)
                timeline.record(world, occupancy)

            world.tick(dt, observations)

            # viewer.render(world, PARKING_ZONES, observations)
            camera_view.render(frame, observations, world, observer.image_points, observer.H_inv)

            time.sleep(dt) # Run updates at 30 FPS
    except KeyboardInterrupt:
        print("Stopping system...")
    
    finally:
        if recorder is not None:
            recorder.save()
            timeline.save()
            print("Observations saved")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

# main should not contain domain logic, just call functions from other modules. The main loop should be as clean as possible, just calling functions and printing results.
# call perception to get observations, call world model to update belief, call logic to compute occupancy, print results.
# main = system pipeline controller.