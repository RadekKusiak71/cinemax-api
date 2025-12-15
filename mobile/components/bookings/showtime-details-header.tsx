import { ShowingDetail } from '@/api/showings';
import { format } from 'date-fns';
import { StyleSheet, Text, View } from "react-native";

type ShowtimeDetailsHeaderProps = {
    details: ShowingDetail;
}

const SEAT_COLORS = {
    SCREEN: '#D3D3D3',
};

export const ShowtimeDetailsHeader = ({ details }: ShowtimeDetailsHeaderProps) => (
    <View style={styles.detailsContainer}>
        <Text style={styles.movieTitle}>{details.movie.title}</Text>
        <Text style={styles.detailText}>
            Hall: **{details.theater_hall}** | Start: **{format(new Date(details.start_time), 'MMM do, HH:mm')}**
        </Text>
        <View style={styles.screenView}>
            <Text style={styles.screenText}>Screen</Text>
        </View>
    </View>
);

const styles = StyleSheet.create({
    detailsContainer: {
        paddingHorizontal: 20,
        paddingBottom: 10,
        alignItems: 'center',
    },
    movieTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 5,
        textAlign: 'center',
    },
    detailText: {
        fontSize: 14,
        color: '#555',
        marginBottom: 15,
    },
    screenView: {
        height: 5,
        width: '80%',
        backgroundColor: SEAT_COLORS.SCREEN,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 20,
        borderRadius: 2,
    },
    screenText: {
        fontSize: 10,
        color: '#fff',
        position: 'absolute',
        top: -15,
    },
});