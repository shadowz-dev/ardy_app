import { View, StyleSheet, Text} from 'react-native';
import { Link, Stack } from 'expo-router';

export default function NotFoundScreen() {
    return (
        <>
            <Stack.Screen options= {{ title: "Oops! Not Found"}}/>
            <View style={styles.container}>
                <Text style={styles.text}>Page not found. Please try again.</Text>
                <Link href="/">
                    <Text style={styles.button}>Go back to Home</Text>
                </Link>
            </View>
        </>
    )
}

const styles = StyleSheet.create({
    container: {
        backgroundColor: '#25292e',
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    text: {
        fontSize: 24,
        color: '#fff',
        marginBottom: 20,
    },
    button: {
        fontSize: 18,
        color: '#fff',
        marginTop: 10,
        padding: 10,
        backgroundColor: 'green',
        borderRadius: 5,
    },
});