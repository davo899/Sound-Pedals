from pygame import *
from davo import Button, Slider
from SoundProcessorClass import SoundProcessor

init()

FPS = 90


class Main:

    def __init__(self):
        self.run = True
        self.clock = time.Clock()
        self.win = display.set_mode((1200, 720))
        self.sound = SoundProcessor()

        self.inputGraphRect = (50, 50, 500, 300)
        self.outputGraphRect = (650, 50, 500, 300)

        self.ampToggleButton = Button(
            (100, 500),
            100, 30,
            caption="Amp",
            border=3,
        )

        self.ampSlider = Slider(
            (100, 600),
            100, 20,
            border=2,
            range_=(0, 10),
            buttonWidth=10,
            default=2
        )

        self.vibratoToggleButton = Button(
            (250, 500),
            100, 30,
            caption="Vibrato",
            border=3,
        )

        self.vibratoSpeedSlider = Slider(
            (250, 600),
            100, 20,
            border=2,
            range_=(0.01, 10),
            buttonWidth=10,
            default=2
        )

        self.vibratoIntensitySlider = Slider(
            (250, 650),
            100, 20,
            border=2,
            range_=(0, 1),
            buttonWidth=10,
            default=1
        )

        self.delayToggleButton = Button(
            (400, 500),
            100, 30,
            caption="Delay",
            border=3,
        )

        self.delaySlider = Slider(
            (400, 600),
            100, 20,
            border=2,
            range_=(0, 2),
            buttonWidth=10,
            default=0.5
        )

    def update(self):
        for even in event.get():
            if even.type == QUIT:
                self.run = False

            if self.ampToggleButton.handleEvent(even):
                self.sound.effects["amp"].toggle()

            if self.vibratoToggleButton.handleEvent(even):
                self.sound.effects["vibrato"].toggle()

            if self.delayToggleButton.handleEvent(even):
                self.sound.effects["delay"].toggle()

            self.ampSlider.handleEvent(even)
            self.vibratoSpeedSlider.handleEvent(even)
            self.vibratoIntensitySlider.handleEvent(even)
            self.delaySlider.handleEvent(even)

            self.sound.effects["amp"].setAmp(self.ampSlider.value)
            self.sound.effects["vibrato"].setSpeed(1/self.vibratoSpeedSlider.value)
            self.sound.effects["vibrato"].setIntensity(self.vibratoIntensitySlider.value)
            self.sound.effects["delay"].setDelay(self.delaySlider.value)

        self.sound.update(FPS, self.clock.get_time()/1000)

        self.win.fill((0, 0, 0))

        draw.lines(
            self.win,
            (255, 0, 0),
            False,
            SoundProcessor.getGraphByFrame(self.sound.inputFrame, self.inputGraphRect),
            3
        )

        draw.lines(
            self.win,
            (0, 255, 0),
            False,
            SoundProcessor.getGraphByFrame(self.sound.currentFrame, self.outputGraphRect),
            3
        )

        draw.rect(self.win, (10, 10, 10), (0, 450, 1200, 270))

        self.ampToggleButton.draw(self.win)
        self.ampSlider.draw(self.win, str(self.ampSlider.value)+"x")

        self.vibratoToggleButton.draw(self.win)
        self.vibratoSpeedSlider.draw(self.win, "Speed: "+str(self.vibratoSpeedSlider.value)+"/s")
        self.vibratoIntensitySlider.draw(self.win, "Intensity: "+str(self.vibratoIntensitySlider.value))

        self.delayToggleButton.draw(self.win)
        self.delaySlider.draw(self.win, "Time: "+str(self.delaySlider.value)+"s")

        display.update()


main = Main()
while main.run:
    main.clock.tick(FPS)
    main.update()

main.sound.stop()
quit()
