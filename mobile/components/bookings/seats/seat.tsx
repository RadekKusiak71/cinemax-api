import { RoomSeat } from "@/api/showings";
import { useCallback } from "react";
import { StyleSheet, Text, TouchableOpacity } from "react-native";

const SEAT_COLORS = {
    AVAILABLE: '#E3342F',
    SELECTED: '#6AA84F',
    RESERVED: '#A9A9A9',
};

type SeatProps = {
    seat: RoomSeat;
    isSelected: boolean;
    onToggle: (seatId: number) => void;
}

const Seat = ({ seat, isSelected, onToggle }: SeatProps) => {
    const isReserved = seat.is_reserved;

    const backgroundColor = isReserved
        ? SEAT_COLORS.RESERVED
        : isSelected
            ? SEAT_COLORS.SELECTED
            : SEAT_COLORS.AVAILABLE;

    const handlePress = useCallback(() => {
        if (!isReserved) {
            onToggle(seat.id);
        }
    }, [isReserved, seat.id, onToggle]);

    return (
        <TouchableOpacity
            testID="seat-touchable"
            style={[styles.seat, { backgroundColor }]}
            onPress={handlePress}
            disabled={isReserved}
        >
            <Text style={styles.seatText}>{seat.number}</Text>
        </TouchableOpacity>
    );
};


const styles = StyleSheet.create({
    seatsGroup: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        marginVertical: 5
    },
    seat: {
        width: 40,
        height: 40,
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: 5,
    },
    seatText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 12,
    },
});

export default Seat;