# Wave-to-scalable-integer

Converts .wav(WAVE) files to integer sequence using a customizable bit-range, i.e. 8-bit range, sound sample sequence values -> 0 - 255 <br>
This could be useful when creating sequences for DACs. 

Sound effects used when building this: [Website to download sounds](https://opengameart.org/content/512-sound-effects-8-bit-style) <br>


This will output a c_sounds.txt file containing the sounds scaled, and made for the struct format shown below:
``` c
struct Sound = {
  uint32_t length;
  uint16_t sampling_freq;
  uint8_t samples[];
}
```

