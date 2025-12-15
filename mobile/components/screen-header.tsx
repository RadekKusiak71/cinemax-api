import React from 'react';
import { Text, View, StyleSheet } from "react-native";
import { theme } from "@/constants/theme";

const ScreenHeader = ({ title }: { title: string }) => {
    return (
        <View style={styles.header}>
            <Text style={styles.title}>{title}</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    header: {
        paddingHorizontal: 20,
        paddingVertical: 15,
        borderBottomWidth: 1,
        borderBottomColor: '#f0f0f0',
    },
    title: {
        fontSize: 32,
        fontWeight: 'bold',
        color: theme.colors.textPrimary,
    },
});

export default ScreenHeader;