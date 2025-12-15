import Button from "@/components/button";
import { theme } from "@/constants/theme";
import React from "react";
import { StyleSheet, Text, View } from "react-native";

type Props = {
    title?: string;
    message?: string;
    onRetry?: () => void;
    retryText?: string;
};

const ErrorScreen: React.FC<Props> = ({
    title = "Oops!",
    message = "Something went wrong.",
    onRetry,
    retryText = "Try again",
}) => {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>{title}</Text>
            <Text style={styles.message}>{message}</Text>

            {onRetry ? (
                <View style={styles.buttonWrap}>
                    <Button title={retryText} onPress={onRetry} isLoading={false} />
                </View>
            ) : null}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: theme.colors.background,
        justifyContent: "center",
        alignItems: "center",
        padding: 24,
        gap: 10,
    },
    title: {
        fontSize: 20,
        fontWeight: "700",
        color: theme.colors.textPrimary,
    },
    message: {
        fontSize: 14,
        color: theme.colors.textPrimary,
        opacity: 0.8,
        textAlign: "center",
    },
    buttonWrap: {
        marginTop: 12,
        width: "100%",
    },
});

export default ErrorScreen;
