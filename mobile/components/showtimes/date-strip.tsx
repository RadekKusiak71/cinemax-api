import { theme } from "@/constants/theme";
import React, { useMemo } from "react";
import { ScrollView, StyleSheet, Text, TouchableOpacity, View } from "react-native";

interface DateStripProps {
    selectedDate: Date;
    onSelectDate: (date: Date) => void;
}

const DateStrip = ({ selectedDate, onSelectDate }: DateStripProps) => {
    const dates = useMemo(() => {
        const days = [];
        const today = new Date();
        for (let i = 0; i < 7; i++) {
            const date = new Date(today);
            date.setDate(today.getDate() + i);
            days.push(date);
        }
        return days;
    }, []);

    const isSameDate = (d1: Date, d2: Date) => {
        return d1.getDate() === d2.getDate() && d1.getMonth() === d2.getMonth();
    };

    return (
        <View style={styles.wrapper}>
            <Text style={styles.label}>Select Date</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.scrollContent}>
                {dates.map((date, index) => {
                    const isSelected = isSameDate(date, selectedDate);
                    const dayName = index === 0 ? "Today" : date.toLocaleDateString('en-US', { weekday: 'short' });
                    const dayNumber = date.getDate();

                    return (
                        <TouchableOpacity
                            key={index}
                            testID={`date-item-${index}`}
                            style={[styles.dateItem, isSelected && styles.dateItemSelected]}
                            onPress={() => onSelectDate(date)}
                        >
                            <Text style={[styles.dayName, isSelected && styles.textSelected]}>{dayName}</Text>
                            <Text style={[styles.dayNumber, isSelected && styles.textSelected]}>{dayNumber}</Text>
                        </TouchableOpacity>
                    );
                })}
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    wrapper: {
        marginVertical: 16,
    },
    label: {
        fontSize: 16,
        fontWeight: '600',
        color: theme.colors.textPrimary,
        marginBottom: 10,
        paddingHorizontal: 16,
    },
    scrollContent: {
        paddingHorizontal: 16,
        gap: 10,
    },
    dateItem: {
        width: 60,
        height: 70,
        borderRadius: 12,
        backgroundColor: '#f4f4f5',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 4,
    },
    dateItemSelected: {
        backgroundColor: theme.colors.primary,
    },
    dayName: {
        fontSize: 12,
        color: theme.colors.textMuted,
        textTransform: 'uppercase',
    },
    dayNumber: {
        fontSize: 18,
        fontWeight: 'bold',
        color: theme.colors.textPrimary,
    },
    textSelected: {
        color: theme.colors.textOnPrimary,
    },
});

export default DateStrip;