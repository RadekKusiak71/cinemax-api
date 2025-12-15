import { useMemo } from "react";
import { ScrollView, StyleSheet, View } from "react-native";
import Seat from "./seat";
import { RoomSeat } from "@/api/showings";

type GroupedSeats = {
    rowIndex: number;
    seats: RoomSeat[];
};

type SeatLayoutProps = {
    seatsData: RoomSeat[];
    selectedSeats: number[];
    onToggleSeat: (seatId: number) => void;
};

export const SeatLayout = ({
    seatsData,
    selectedSeats,
    onToggleSeat,
}: SeatLayoutProps) => {
    const groupedSeats: GroupedSeats[] = useMemo(() => {
        const groups = seatsData.reduce((acc, seat) => {
            const rowIndex = seat.row;
            if (!acc[rowIndex]) {
                acc[rowIndex] = { rowIndex, seats: [] };
            }
            acc[rowIndex].seats.push(seat);
            return acc;
        }, {} as Record<number, GroupedSeats>);

        return Object.values(groups)
            .sort((a, b) => a.rowIndex - b.rowIndex)
            .map((group) => ({
                ...group,
                seats: group.seats.sort((a, b) => a.number - b.number),
            }));
    }, [seatsData]);

    return (
        <ScrollView
            horizontal
            contentContainerStyle={styles.contentContainer}
            showsHorizontalScrollIndicator={false}
        >
            {groupedSeats.map((row) => (
                <View style={styles.seatsGroup} key={row.rowIndex}>
                    {row.seats.map((seat) => (
                        <Seat
                            key={seat.id}
                            seat={seat}
                            isSelected={selectedSeats.includes(seat.id)}
                            onToggle={onToggleSeat}
                        />
                    ))}
                </View>
            ))}
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    contentContainer: {
        flexDirection: "column",
        paddingHorizontal: 8,
        gap: 12,
    },
    seatsGroup: {
        flexDirection: "row",
        justifyContent: "space-evenly",
        marginVertical: 5,
        gap: 8,
    },
    seat: {
        width: 40,
        height: 40,
        alignItems: "center",
        justifyContent: "center",
        borderRadius: 5,
    },
    seatText: {
        color: "#fff",
        fontWeight: "bold",
        fontSize: 12,
    },
});
