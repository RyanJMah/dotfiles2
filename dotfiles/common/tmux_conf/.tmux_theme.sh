#!/usr/bin/env bash

# Color Pallette
white='#fcfcfa'
black='#24292e'
gray='#2d2d2d'
red='#ff668c'
green='#7bd88f'
yellow='#fed484'
blue='#79b8ff'
magenta='#ac82cb'
cyan='#5ad4e6'

# Handle left icon configuration
left_icon="#I"

# Handle left icon padding
padding=""
if [ "$show_left_icon_padding" -gt "0" ]; then
padding="$(printf '%*s' $show_left_icon_padding)"
fi
left_icon="$left_icon$padding"

# set length
tmux set-option -g status-left-length 100
tmux set-option -g status-right-length 100

# pane border styling
tmux set-option -g pane-active-border-style "fg=${red}"
tmux set-option -g pane-border-style "fg=${gray}"

# message styling
tmux set-option -g message-style "bg=${gray},fg=${white}"

# status bar
tmux set-option -g status-style "bg=${gray},fg=${white}"

# Status left
tmux set-option -g status-left "#[fg=${red},bg=${black}]#{?client_prefix,#[fg=${yellow}],}#[bg=${red},fg=${black},bold]#{?client_prefix,#[bg=${yellow}],} ${left_icon} #[fg=${red},bg=${gray}]#{?client_prefix,#[fg=${yellow}],}${left_sep}"
powerbg=${gray}

# Status right
tmux set-option -g status-right ""


tmux set-option -ga status-right "#[fg=${!colors[0]},bg=${powerbg},nobold,nounderscore,noitalics]${right_sep}#[fg=${!colors[1]},bg=${!colors[0]}] $script "
powerbg=${!colors[0]}

tmux set-option -ga status-right "#[fg=${green},bg=${yellow}]${right_sep}#[bg=${green},fg=${black},bold] #h #[bg=${black},fg=${green}]"
tmux set-window-option -g window-status-current-format "#[bg=${white},fg=${gray}]${left_sep} #[fg=${black},bg=${white}]#I #W${current_flags} #[bg=${gray},fg=${white}]${left_sep}"

tmux set-window-option -g window-status-format "#[bg=${gray},fg=${gray}]${left_sep} #[fg=${white},bg=${gray}]#I #W${flags} #[bg=${gray},fg=${gray}]${left_sep}"
tmux set-window-option -g window-status-activity-style "bold"
tmux set-window-option -g window-status-bell-style "bold"
tmux set-window-option -g window-status-separator ""

# Set to top
tmux set-option -g status-position top
