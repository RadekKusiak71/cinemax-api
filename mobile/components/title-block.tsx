import { theme } from "@/constants/theme";
import { StyleSheet, Text, View } from "react-native";

type TitleBlockProps = {
    title: string,
    subtitle: string | number,
};

const TitleBlock: React.FC<TitleBlockProps> = ({ title, subtitle }) => {
    return (
        <View>
            <Text style={styles.titleText}>{title}</Text>
            <Text style={styles.subtitleText}>{subtitle}</Text>
        </View>
    )
};

const styles = StyleSheet.create({
    titleText: {
        fontSize: 28,
        fontWeight: 'bold',
        color: theme.colors.textPrimary,
        marginBottom: 5,
    },
    subtitleText: {
        fontSize: 16,
        color: theme.colors.textMuted,
    },
});

export default TitleBlock;