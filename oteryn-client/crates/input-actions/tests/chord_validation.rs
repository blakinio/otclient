use oteryn_input_actions::{InputAtom, InputChord, InputError, KeyCode, Modifiers, WheelDirection};

#[test]
fn wheel_direction_cannot_be_combined_with_held_inputs() {
    assert_eq!(
        InputChord::new(
            Modifiers::NONE,
            vec![
                InputAtom::Key(KeyCode::KEY_A),
                InputAtom::Wheel(WheelDirection::Up),
            ],
        ),
        Err(InputError::InvalidWheelChord)
    );
}

#[test]
fn multiple_wheel_directions_cannot_form_one_chord() {
    assert_eq!(
        InputChord::new(
            Modifiers::NONE,
            vec![
                InputAtom::Wheel(WheelDirection::Up),
                InputAtom::Wheel(WheelDirection::Right),
            ],
        ),
        Err(InputError::InvalidWheelChord)
    );
}
