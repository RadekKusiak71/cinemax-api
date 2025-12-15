import { useCreateReservation } from '@/api/reservations';
import { useRoomLayout, useShowingDetail } from '@/api/showings';
import { BookingFooter } from '@/components/bookings/booking-footer';
import { SeatLayout } from '@/components/bookings/seats/seats-layout';
import { ShowtimeDetailsHeader } from '@/components/bookings/showtime-details-header';
import ErrorScreen from "@/components/ui/error-screen";
import LoadingScreen from "@/components/ui/loading-screen";
import { useAuth } from "@/context/auth-context";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useState } from "react";
import { Alert, StyleSheet } from "react-native";
import { SafeAreaView } from 'react-native-safe-area-context';

const SeatSelectionView = () => {
    const router = useRouter();
    const [selectedSeats, setSelectedSeats] = useState<number[]>([]);
    const { isAuthenticated } = useAuth();

    const { showtime_id } = useLocalSearchParams();
    const numericShowtimeId = Number(showtime_id);

    const isShowtimeIdValid = Number.isFinite(numericShowtimeId) && numericShowtimeId > 0;

    const {
        data: seatsData,
        isLoading: isLoadingSeats,
        isError: isErrorSeats
    } = useRoomLayout(numericShowtimeId);

    const {
        data: showtimeDetails,
        isLoading: isLoadingDetails,
        isError: isErrorDetails
    } = useShowingDetail(numericShowtimeId);

    const {
        mutate: createReservation,
        isPending: isCreatingReservation,
    } = useCreateReservation();

    const toggleSeat = (seatId: number) => {
        if (selectedSeats.length === 6 && !selectedSeats.includes(seatId)) {
            Alert.alert("You can select a maximum of 6 seats.");
            return;
        }

        setSelectedSeats(prev =>
            prev.includes(seatId)
                ? prev.filter(id => id !== seatId)
                : [...prev, seatId]
        );
    };

    const handleBookSeats = () => {
        if (!isAuthenticated) {
            Alert.alert("You need to be logged in to make a reservation.");
            router.push({
                pathname: "/(auth)/login-view",
                params: {
                    redirect: encodeURIComponent(`/${numericShowtimeId}/seat-selection-view`),
                },
            } as any);
            return;
        }

        if (!isShowtimeIdValid) {
            Alert.alert("Invalid showtime. Please go back and select a showtime again.");
            return;
        }

        if (selectedSeats.length === 0) {
            Alert.alert("Please select at least one seat.");
            return;
        }

        createReservation(
            { showing_id: numericShowtimeId, seat_ids: selectedSeats },
            {
                onSuccess: (data) => {
                    setSelectedSeats([]);
                    console.log(data);
                    router.push({
                        pathname: "/reservation/[booking_id]/reservation-details-view",
                        params: { booking_id: String(data.id), showtime_id: String(numericShowtimeId) },
                    } as any);
                },
                onError: (error: any) => {
                    const message =
                        (error?.response?.data?.detail as string) ||
                        (error instanceof Error ? error.message : "Unknown error");
                    Alert.alert("Failed to create reservation. Please try again.", message);
                },
            }
        );
    };

    if (!isShowtimeIdValid) {
        return <ErrorScreen message="Invalid showtime. Please go back and select a showtime again." />;
    }

    if (isLoadingSeats || isLoadingDetails) {
        return (
            <LoadingScreen message="Loading seat layout and showtime details..." />
        );
    }

    if (isErrorSeats || !seatsData || isErrorDetails) {
        return (
            <ErrorScreen message="Failed to load showtime data. Please try again later." />
        );
    }

    if (!showtimeDetails) {
        return <ErrorScreen message="Showtime details not found." />;
    }

    return (
        <SafeAreaView style={styles.container}>
            <ShowtimeDetailsHeader details={showtimeDetails} />

            <SeatLayout
                seatsData={seatsData}
                selectedSeats={selectedSeats}
                onToggleSeat={toggleSeat}
            />

            <BookingFooter
                selectedCount={selectedSeats.length}
                onBookSeats={handleBookSeats}
                isLoading={isCreatingReservation}
            />
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        padding: 10,
    },
});

export default SeatSelectionView;
