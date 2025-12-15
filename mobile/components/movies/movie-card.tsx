import { Movie } from '@/api/movies';
import { theme } from '@/constants/theme';
import { Image } from 'expo-image';
import { StyleSheet, Text, TouchableOpacity } from 'react-native';

type MovieCardProps = {
    movie: Movie;
    onPress: () => void;
};

const blurhash = '|rF?hV%2WCj[ayj[a|j[az_NaeWBj@ayfRayfQfQM{M|azj[azf6fQfQfQIpWXofj[ayj[j[fQayWCoeoeaya}j[ayfQa{oLj?j[WVj[ayayj[fQoff7azayj[ayj[j[ayofayayayj[fQj[ayayj[ayfjj[j[ayjuayj[';

const MovieCard = ({ movie, onPress }: MovieCardProps) => {
    return (
        <TouchableOpacity key={movie.id} style={styles.container} onPress={onPress}>
            <Image
                style={styles.image}
                source={{ uri: movie.poster_image }}
                placeholder={{ blurhash }}
                contentFit="cover"
                transition={1000}
                accessibilityLabel={`${movie.title} poster`}
            />

            <Text style={styles.title} numberOfLines={1}>
                {movie.title}
            </Text>
            <Text style={styles.releaseYear}>
                {movie.release_year}
            </Text>
        </TouchableOpacity>
    )
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        gap: 8,
        marginBottom: 16,
    },
    image: {
        height: 250,
        borderRadius: 12,
        backgroundColor: theme.colors.background,
    },
    title: {
        fontSize: 16,
        fontWeight: '700',
        color: theme.colors.textPrimary || '#000',
        marginTop: 4,
        paddingLeft: 5,
    },
    releaseYear: {
        fontSize: 13,
        color: theme.colors.textMuted || '#666',
        paddingLeft: 5,
    },
});

export default MovieCard;