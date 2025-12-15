import ButtonLink from "@/components/button-link";
import { theme } from "@/constants/theme";
import { StatusBar, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const WelcomeView = () => {
	return (
		<SafeAreaView style={styles.container}>

			<StatusBar barStyle='dark-content' />

			<View style={styles.welcomeHeader}>
				<Text style={styles.welcomeHeaderTitle}>Welcome To Cinemax</Text>
				<Text style={styles.welcomeHeaderSubText}>Select cinema, find your movie and book your tickets</Text>
			</View>

			<View style={styles.welcomeButtonsContainer}>
				<View style={styles.welcomeUpperButtonsContainer}>
					<ButtonLink text='Sign Up' href='/(auth)/register-view' style={styles.buttonFlex} />
					<ButtonLink text='Sign In' href='/(auth)/login-view' style={[styles.buttonFlex, styles.buttonSpacing]} />
				</View>
				<ButtonLink text='Continue as Guest' href='/(dashboard)/movies-list-view' variant='secondary' />
			</View>
		</SafeAreaView>
	)
};

const styles = StyleSheet.create({
	container: {
		flex: 1,
		justifyContent: 'space-between',
		padding: 20,
		backgroundColor: theme.colors.background,
	},
	welcomeHeader: {
		marginTop: 40,
		gap: 4
	},
	welcomeHeaderTitle: {
		textAlign: 'center',
		fontSize: 28,
		fontWeight: 'bold',
	},
	welcomeHeaderSubText: {
		textAlign: 'center',
		fontSize: 16,
		color: theme.colors.textMuted,
	},
	welcomeButtonsContainer: {
		gap: 12,
	},
	welcomeUpperButtonsContainer: {
		flexDirection: 'row',
		width: '100%',
	},
	buttonFlex: {
		flex: 1,
	},
	buttonSpacing: {
		marginLeft: 10,
	}
});

export default WelcomeView;