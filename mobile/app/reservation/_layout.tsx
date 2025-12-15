import { Stack } from "expo-router";

const ReservationLayout = () => {
    return (
        <Stack initialRouteName="[booking_id]/reservation-details-view">
            <Stack.Screen name="[booking_id]/reservation-details-view" options={{ headerShown: false }} />
            <Stack.Screen name="[booking_id]/confirmed-reservation-details-view" options={{ headerShown: false }} />
        </Stack>
    );
};

export default ReservationLayout;
