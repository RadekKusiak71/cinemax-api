import { AuthProvider, useAuth } from "@/context/auth-context";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Stack } from "expo-router";

const Layout = () => {
	const { isAuthenticated } = useAuth();

	return (
		<Stack>
			<Stack.Protected guard={!isAuthenticated}>
				<Stack.Screen name='(auth)' options={{ headerShown: false }} />
				<Stack.Screen name='index' options={{ headerShown: false }} />
			</Stack.Protected>
			<Stack.Screen name='(dashboard)' options={{ headerShown: false }} />
			<Stack.Screen name='[movie_id]/movie-details-view' options={{ headerShown: false }} />
			<Stack.Screen name='[showtime_id]' options={{ headerShown: false }} />
			<Stack.Screen name='reservation' options={{ headerShown: false }} />
			<Stack.Screen name='payment-return' options={{ headerShown: false }} />
		</Stack >
	)
};

const RootLayout = () => {
	return (
		<QueryClientProvider client={new QueryClient()}>
			<AuthProvider>
				<Layout />
			</AuthProvider>
		</QueryClientProvider>
	)
};

export default RootLayout;