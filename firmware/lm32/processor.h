#ifndef __PROCESSOR_H
#define __PROCESSOR_H

#define PROCESSOR_MODE_COUNT 10
#define PROCESSOR_MODE_DESCLEN 32

enum {
	VIDEO_IN_HDMI_IN0=0,
	VIDEO_IN_HDMI_IN1
};

extern int processor_mode;
int processor_h_active;
int processor_v_active;
int processor_hdmi_out0_source;
int processor_hdmi_out1_source;
int processor_encoder_source;

void processor_list_modes(char *mode_descriptors);
void processor_start(int mode);
void processor_set_hdmi_out0_source(int source);
void processor_set_hdmi_out1_source(int source);
void processor_set_encoder_source(int source);
void processor_update(void);
void processor_service(void);

#endif /* __VIDEOMODE_H */
