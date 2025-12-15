import { theme } from "@/constants/theme";
import { StyleSheet, Text, View } from "react-native";
import Button from "../button";

const SEAT_COLORS = {
    AVAILABLE: '#E3342F',
    SELECTED: '#6AA84F',
    RESERVED: '#A9A9A9'
};

type LegendItemProps = {
    color: string;
    text: string;
}

const LegendItem = ({ color, text }: LegendItemProps) => (
    <View style={styles.legendItem}>
        <View style={[styles.legendColor, { backgroundColor: color }]} />
        <Text style={styles.legendText}>{text}</Text>
    </View>
);

type BookingFooterProps = {
    selectedCount: number;
    isLoading?: boolean;
    onBookSeats: () => void;
}

export const BookingFooter = ({ selectedCount, isLoading, onBookSeats }: BookingFooterProps) => {
    return (
        <View style={styles.footer}>
            <View style={styles.legendContainer}>
                <LegendItem color={SEAT_COLORS.AVAILABLE} text="Available" />
                <LegendItem color={SEAT_COLORS.SELECTED} text="Selected" />
                <LegendItem color={SEAT_COLORS.RESERVED} text="Reserved" />
            </View>

            <Text style={styles.selectedSeatsText}>
                **{selectedCount}** seat(s) selected
            </Text>

            <View style={styles.bookButton}>
                <Button title="Book Selected Seats" onPress={onBookSeats} isLoading={isLoading} disabled={selectedCount === 0 || isLoading} />
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    footer: {
        padding: 20,
        borderTopWidth: 1,
        borderTopColor: '#eee',
        alignItems: 'center',
    },
    legendContainer: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        width: '80%',
        marginBottom: 15,
    },
    legendItem: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    legendColor: {
        width: 15,
        height: 15,
        borderRadius: 3,
        marginRight: 5,
    },
    legendText: {
        fontSize: 12,
        color: '#555',
    },
    selectedSeatsText: {
        fontSize: 14,
        fontWeight: '600',
        marginBottom: 10,
    },
    bookButton: {
        width: '100%',
        backgroundColor: theme.colors.primary,
        borderRadius: 8,
        alignItems: 'center',
    },
    bookButtonText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
    },
});