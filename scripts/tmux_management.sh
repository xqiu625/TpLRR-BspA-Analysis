#!/bin/bash
#
# Script to manage tmux sessions for running LRR pattern analyses
#

function usage {
    echo "Usage: $0 [create|attach|list|kill] [session_name]"
    echo
    echo "Commands:"
    echo "  create [session_name]  - Create a new tmux session"
    echo "  attach [session_name]  - Attach to an existing tmux session"
    echo "  list                   - List all active tmux sessions"
    echo "  kill [session_name]    - Kill a specific tmux session"
    echo
    echo "Example:"
    echo "  $0 create tplrr_analysis"
    echo "  $0 list"
    echo "  $0 attach tplrr_analysis"
    echo "  $0 kill tplrr_analysis"
}

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "Error: tmux is not installed. Please install tmux first."
    exit 1
fi

# Check for command
if [ $# -lt 1 ]; then
    usage
    exit 1
fi

COMMAND=$1
SESSION_NAME=$2

case $COMMAND in
    create)
        if [ -z "$SESSION_NAME" ]; then
            echo "Error: Session name is required."
            usage
            exit 1
        fi
        
        # Check if session already exists
        if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
            echo "Session '$SESSION_NAME' already exists."
            echo "Use 'attach' command to connect to it."
            exit 1
        fi
        
        # Create new session
        tmux new-session -d -s "$SESSION_NAME"
        echo "Created new session: $SESSION_NAME"
        echo "Use '$0 attach $SESSION_NAME' to connect to it."
        echo "Press Ctrl+B then D to detach from the session without stopping it."
        
        # Automatically attach to the new session
        tmux attach-session -t "$SESSION_NAME"
        ;;
        
    attach)
        if [ -z "$SESSION_NAME" ]; then
            echo "Error: Session name is required."
            usage
            exit 1
        fi
        
        # Check if session exists
        if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
            echo "Error: Session '$SESSION_NAME' does not exist."
            echo "Use 'list' command to see active sessions."
            exit 1
        fi
        
        # Attach to session
        tmux attach-session -t "$SESSION_NAME"
        ;;
        
    list)
        # List all sessions
        echo "Active tmux sessions:"
        tmux list-sessions
        ;;
        
    kill)
        if [ -z "$SESSION_NAME" ]; then
            echo "Error: Session name is required."
            usage
            exit 1
        fi
        
        # Check if session exists
        if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
            echo "Error: Session '$SESSION_NAME' does not exist."
            echo "Use 'list' command to see active sessions."
            exit 1
        fi
        
        # Kill session
        tmux kill-session -t "$SESSION_NAME"
        echo "Killed session: $SESSION_NAME"
        ;;
        
    *)
        echo "Error: Unknown command '$COMMAND'"
        usage
        exit 1
        ;;
esac

exit 0
