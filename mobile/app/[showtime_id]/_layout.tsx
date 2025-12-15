import { Stack } from "expo-router";



const BookingLayout = () => {
    return (
        <Stack initialRouteName='seat-selection-view'>
            <Stack.Screen name='seat-selection-view' options={{ headerShown: false }} />
        </Stack>
    )
};

export default BookingLayout;