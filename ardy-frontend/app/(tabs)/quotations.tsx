import { Text, View, StyleSheet } from 'react-native';

export default function QuotationsScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Quotations screen</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#2d363b',
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: '#fff',
  },
});
