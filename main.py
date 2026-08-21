from axon.core.application import Application
from axon.core.dummy_service import DummyService

def main():
    app = Application()
    app.register_service(DummyService())
    
    try:
        app.run()
        app.wait()
    except KeyboardInterrupt:
        app.stop()

if __name__ == "__main__":
    main()