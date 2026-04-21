from state.world_model import WorldModel
from geometry.zones import PARKING_ZONES
from logic.occupancy_engine import OccupancyEngine
from debug.topdown_view import TopDownView
from replay.recorder import ObservationRecorder
from replay.player import ObservationPlayer
from debug.timeline import TimelineRecorder
from perception.camera_observer import CameraObserver
from api.state_store import state_store
from debug.camera_view import CameraView
import cv2

camera_view = CameraView()
viewer = TopDownView()
occupancy_engine = OccupancyEngine()
timeline = TimelineRecorder()

MODE = "record"
# MODE = "replay"

if MODE == "record":
    observer = CameraObserver()
    recorder = ObservationRecorder("observations.json")

elif MODE == "replay":
    observer = ObservationPlayer("observations.json")
    recorder = None

def main():
    world = WorldModel()

    try:
        while True:
            observations, frame = observer.get_observations()
            dt = observer.dt

            if frame is None:
                break

            # update world
            world.tick(dt, observations)

            # compute occupancy
            occupancy = occupancy_engine.update(world, PARKING_ZONES, dt)

            state_store.occupancy = occupancy
            state_store.entities = [
                {
                    "entity_id": e.entity_id,
                    "position": e.position,
                    "velocity": e.velocity
                }
                for e in world.entities.values()
            ]

            if recorder is not None:
                recorder.record(observations)
                timeline.record(world, occupancy)

            # render
            viewer.render(frame, observations, world, PARKING_ZONES, occupancy)
            camera_view.render(frame, observations, world, observer.image_points, observer.H_inv)

            key = cv2.waitKey(1) & 0xFF

            if key == 27:  # ESC key
                print("ESC pressed. Stopping system...")
                break

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

# call perception to get observations, call world model to update belief, call logic to compute occupancy, print results.
# main = system pipeline controller.