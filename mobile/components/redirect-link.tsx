import { theme } from "@/constants/theme";
import { Link, LinkProps } from "expo-router";
import React from "react";
import { StyleSheet, Text } from "react-native";


interface RedirectLinkProps extends LinkProps {
    text?: string;
    linkText: string;
}

const RedirectLink: React.FC<RedirectLinkProps> = ({ text, linkText, ...props }) => {
    return (
        <Text style={styles.text}>
            {text}<Link {...props} style={styles.linkText}>{linkText}</Link>
        </Text>
    );
};

const styles = StyleSheet.create({
    text: {
        color: theme.colors.textMuted,
        fontWeight: "600",
    },
    linkText: {
        color: theme.colors.primary,
        fontWeight: "700",
    }
});


export default RedirectLink;