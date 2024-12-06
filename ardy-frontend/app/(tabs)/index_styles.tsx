import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
      backgroundColor: '#2d363b',
      paddingBottom: 20,
    },
    header: {
      flexDirection: 'row', // Align logo and welcome container in a row
      alignItems: 'center', // Vertically align content
      padding: 10,
      marginTop: 10,
      marginBottom: 30, // Add spacing between header and next section
    },
    logoContainer: {
      marginRight: 10, // Add space between the logo and welcome text
    },
    logo: {
      width: 70,
      height: 70,
      borderRadius: 10,
    },
    welcomeContainer: {
      flex: 1, // Take remaining space
    },
    titleWrapper: {
      flexDirection: 'row', // Align title and titleAccent horizontally
    },
    title: {
      fontSize: 20,
      fontWeight: 'bold',
      color: '#fff',
    },
    titleAccent: {
      fontSize: 20,
      fontWeight: 'bold',
      color: '#8ee7e4',
    },
    subtitle: {
      fontSize: 14,
      color: '#fff',
      marginTop: 5,
    },
    sliderSection: {
      marginTop: 20,
      paddingHorizontal: 10,
    },
    sectionTitleWrapper: {
      flexDirection: 'row', // Align main and accent title horizontally
      marginBottom: 10, // Add spacing below the title
    },
    sectionTitle: {
      fontSize: 18,
      fontWeight: 'bold',
      color: '#fff',
    },
    sectionTitleAccent: {
      fontSize: 18,
      fontWeight: 'bold',
      color: '#8ee7e4',
    },
    slider: {
      flexDirection: 'row',
    },
    card: {
      backgroundColor: '#615e5c3c',
      borderRadius: 8,
      padding: 20,
      marginRight: 15,
      alignItems: 'center',
      justifyContent: 'flex-start',
      width: 150,
      height: 150,
    },
    cardText: {
      color: '#fff',
      fontSize: 14,
      textAlign: 'center',
      marginBottom: 10,
    },
    stars: {
      backgroundColor: 'transparent',
      marginBottom: 10,
    },
    username: {
      color: '#ccc',
      fontSize: 12,
      fontStyle: 'italic',
      textAlign: 'center',
    },
    servicesSection: {
      marginTop: 20,
      paddingHorizontal: 15,
    },
    serviceCard: {
      backgroundColor: '#615e5c3c',
      borderRadius: 8,
      padding: 20,
      marginBottom: 15,
      shadowOpacity: 0.5,
      shadowRadius: 5,
    },
    serviceTitle: {
      fontSize: 16,
      fontWeight: 'bold',
      color: '#fff',
      marginBottom: 5,
    },
    serviceDescription: {
      fontSize: 14,
      color: '#ddd',
    },
    ratingContainer: {
      marginBottom: 5,
    },
    providerLogo: {
      width: 70,
      height: 70,
      borderRadius: 35, // Make the logo circular
      marginBottom: 10, // Space between logo and name
    },
  
    refreshIconContainer: {
      alignItems: 'center',
      marginTop: 20,
    },
    refreshIcon: {
      width: 50,
      height: 50,
      marginBottom: 10,
    },
    refreshLogo: {
      width: 50,
      height: 50,
      marginBottom: 5,
      borderRadius: 50,
    },
    pullDownText: {
      fontSize: 14,
      color: '#cccccc',
    },
    pullDownContainer: {
      alignItems: 'center',
      marginBottom: 10,
    },
  });