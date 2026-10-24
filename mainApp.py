import streamlit as st                                                                        
                                                                                              
                                                                                              
# -------------------- ROUTES (IN-MEMORY STORAGE) --------------------                        
                                                                                              
                                                                                              
routes = [                                                                                    
    {                                                                                         
        "route_id": "R101",                                                                   
        "departure": "Karachi",                                                               
        "destination": "Hyderabad",                                                           
        "time": "08:00 AM",                                                                   
        "fare": 1200,                                                                         
        "seats": 40                                                                           
    },                                                                                        
    {                                                                                         
        "route_id": "R102",                                                                   
        "departure": "Karachi",                                                               
        "destination": "Sukkur",                                                              
        "time": "09:30 AM",                                                                   
        "fare": 2000,                                                                         
        "seats": 36                                                                           
    },                                                                                        
    {                                                                                         
        "route_id": "R103",                                                                   
        "departure": "Hyderabad",                                                             
        "destination": "Mirpur Khas",                                                         
        "time": "11:00 AM",                                                                   
        "fare": 800,                                                                          
        "seats": 32                                                                           
    },                                                                                        
    {                                                                                         
        "route_id": "R104",                                                                   
        "departure": "Karachi",                                                               
        "destination": "Lahore",                                                              
        "time": "07:00 PM",                                                                   
        "fare": 5000,                                                                         
        "seats": 45                                                                           
    },                                                                                        
    {                                                                                         
        "route_id": "R105",                                                                   
        "departure": "Sukkur",                                                                
        "destination": "Hyderabad",                                                           
        "time": "02:00 PM",                                                                   
        "fare": 1500,                                                                         
        "seats": 30                                                                           
    }                                                                                         
]                                                                                             
                                                                                              
                                                                                              
# Bookings are also stored in memory.                                                         
# Streamlit session_state keeps them available between normal page reruns.                    
if "bookings" not in st.session_state:                                                        
    st.session_state.bookings = []                                                            
                                                                                              
                                                                                              
if "next_booking_number" not in st.session_state:                                             
    st.session_state.next_booking_number = 1                                                  
                                                                                              
                                                                                              
if "routes_data" not in st.session_state:                                                     
    st.session_state.routes_data = routes                                                     
                                                                                              
                                                                                              
                                                                                              
                                                                                              
# -------------------- HELPER FUNCTIONS --------------------                                  
                                                                                              
                                                                                              
def find_route(route_id):                                                                     
    for route in st.session_state.routes_data:                                                
        if route["route_id"].lower() == route_id.lower():                                     
            return route                                                                      
    return None                                                                               
                                                                                              
                                                                                              
                                                                                              
                                                                                              
def view_routes():                                                                            
    st.subheader("All Bus Routes")                                                            
                                                                                              
                                                                                              
    route_rows = []                                                                           
    for route in st.session_state.routes_data:                                                
        route_rows.append({                                                                   
            "Route ID": route["route_id"],                                                    
            "Departure": route["departure"],                                                  
            "Destination": route["destination"],                                              
            "Departure Time": route["time"],                                                  
            "Fare (PKR)": route["fare"],                                                      
            "Available Seats": route["seats"]                                                 
        })                                                                                    
                                                                                              
                                                                                              
    st.table(route_rows)                                                                      
                                                                                              
                                                                                              
                                                                                              
                                                                                              
def search_routes():                                                                          
    st.subheader("Search Routes")                                                             
                                                                                              
                                                                                              
    search_type = st.selectbox(                                                               
        "Search by",                                                                          
        ["Route ID", "Departure City", "Destination City"]                                    
    )                                                                                         
    search_text = st.text_input("Enter your search")                                          
                                                                                              
                                                                                              
    if st.button("Search"):                                                                   
        if search_text.strip() == "":                                                         
            st.error("Please enter something to search.")                                     
        else:                                                                                 
            found_routes = []                                                                 
                                                                                              
                                                                                              
            for route in st.session_state.routes_data:                                        
                if search_type == "Route ID":                                                 
                    if search_text.lower() == route["route_id"].lower():                      
                        found_routes.append(route)                                            
                elif search_type == "Departure City":                                         
                    if search_text.lower() in route["departure"].lower():                     
                        found_routes.append(route)                                            
                elif search_type == "Destination City":                                       
                    if search_text.lower() in route["destination"].lower():                   
                        found_routes.append(route)                                            
                                                                                              
                                                                                              
            if len(found_routes) == 0:                                                        
                st.warning("No routes found.")                                                
            else:                                                                             
                result_rows = []                                                              
                for route in found_routes:                                                    
                    result_rows.append({                                                      
                        "Route ID": route["route_id"],                                        
                        "Departure": route["departure"],                                      
                        "Destination": route["destination"],                                  
                        "Time": route["time"],                                                
                        "Fare (PKR)": route["fare"],                                          
                        "Available Seats": route["seats"]                                     
                    })                                                                        
                st.table(result_rows)                                                         
                                                                                              
                                                                                              
                                                                                              
                                                                                              
def book_ticket():                                                                            
    st.subheader("Book a Ticket")                                                             
                                                                                              
                                                                                              
    with st.form("booking_form"):                                                             
        passenger_name = st.text_input("Passenger Name")                                      
        passenger_age = st.number_input(                                                      
            "Passenger Age", min_value=1, max_value=120, step=1                               
        )                                                                                     
                                                                                              
                                                                                              
        route_ids = []                                                                        
        for route in st.session_state.routes_data:                                            
            route_ids.append(route["route_id"])                                               
                                                                                              
                                                                                              
        selected_route_id = st.selectbox("Select Route", route_ids)                           
        number_of_seats = st.number_input(                                                    
            "Number of Seats", min_value=1, step=1                                            
        )                                                                                     
                                                                                              
                                                                                              
        submitted = st.form_submit_button("Book Ticket")                                      
                                                                                              
                                                                                              
    if submitted:                                                                             
        if passenger_name.strip() == "":                                                      
            st.error("Passenger name cannot be empty.")                                       
            return                                                                            
                                                                                              
                                                                                              
        selected_route = find_route(selected_route_id)                                        
                                                                                              
                                                                                              
        if selected_route is None:                                                            
            st.error("Invalid route.")                                                        
        elif number_of_seats <= 0:                                                            
            st.error("Number of seats must be greater than zero.")                            
        elif number_of_seats > selected_route["seats"]:                                       
            st.error("Not enough seats available.")                                           
        else:                                                                                 
            booking_id = "B" + str(st.session_state.next_booking_number)                      
            st.session_state.next_booking_number += 1                                         
                                                                                              
                                                                                              
            total_fare = selected_route["fare"] * number_of_seats                             
                                                                                              
                                                                                              
            booking = {                                                                       
                "booking_id": booking_id,                                                     
                "passenger_name": passenger_name.strip(),                                     
                "passenger_age": int(passenger_age),                                          
                "route_id": selected_route["route_id"],                                       
                "departure": selected_route["departure"],                                     
                "destination": selected_route["destination"],                                 
                "number_of_seats": int(number_of_seats),                                      
                "total_fare": total_fare,                                                     
                "status": "Confirmed"                                                         
            }                                                                                 
                                                                                              
                                                                                              
            st.session_state.bookings.append(booking)                                         
            selected_route["seats"] -= int(number_of_seats)                                   
                                                                                              
                                                                                              
            st.success("Ticket booked successfully!")                                         
            st.write("Booking ID:", booking_id)                                               
            st.write("Passenger:", passenger_name.strip())                                    
            st.write("Route:", selected_route["departure"], "to", selected_route["destination"])
            st.write("Seats:", int(number_of_seats))                                          
            st.write("Total Fare: PKR", total_fare)                                           
            st.write("Please save your booking ID for cancellation.")                         
                                                                                              
                                                                                              
                                                                                              
                                                                                              
def view_bookings():                                                                          
    st.subheader("Booking History")                                                           
                                                                                              
                                                                                              
    if len(st.session_state.bookings) == 0:                                                   
        st.info("No bookings have been made yet.")                                            
    else:                                                                                     
        booking_rows = []                                                                     
        for booking in st.session_state.bookings:                                             
            booking_rows.append({                                                             
                "Booking ID": booking["booking_id"],                                          
                "Passenger": booking["passenger_name"],                                       
                "Age": booking["passenger_age"],                                              
                "Route": booking["route_id"],                                                 
                "Departure": booking["departure"],                                            
                "Destination": booking["destination"],                                        
                "Seats": booking["number_of_seats"],                                          
                "Total Fare (PKR)": booking["total_fare"],                                    
                "Status": booking["status"]                                                   
            })                                                                                
        st.table(booking_rows)                                                                
                                                                                              
                                                                                              
                                                                                              
                                                                                              
def cancel_ticket():                                                                          
    st.subheader("Cancel a Ticket")                                                           
                                                                                              
                                                                                              
    booking_id_input = st.text_input("Enter Booking ID", key="cancel_booking_id")             
                                                                                              
                                                                                              
    if st.button("Cancel Ticket"):                                                            
        if booking_id_input.strip() == "":                                                    
            st.error("Please enter a booking ID.")                                            
            return                                                                            
                                                                                              
                                                                                              
        found_booking = None                                                                  
                                                                                              
                                                                                              
        for booking in st.session_state.bookings:                                             
            if booking["booking_id"].lower() == booking_id_input.strip().lower():             
                found_booking = booking                                                       
                break                                                                         
                                                                                              
                                                                                              
        if found_booking is None:                                                             
            st.error("Booking ID not found.")                                                 
        elif found_booking["status"] == "Cancelled":                                          
            st.warning("This ticket has already been cancelled.")                             
        else:                                                                                 
            found_booking["status"] = "Cancelled"                                             
                                                                                              
                                                                                              
            route = find_route(found_booking["route_id"])                                     
            if route is not None:                                                             
                route["seats"] += found_booking["number_of_seats"]                            
                                                                                              
                                                                                              
            st.success("Ticket cancelled successfully.")                                      
            st.write("Booking ID:", found_booking["booking_id"])                              
            st.write("Seats have been restored.")                                             
                                                                                              
                                                                                              
                                                                                              
                                                                                              
def filter_available_routes():                                                                
    st.subheader("Routes by Seat Availability")                                               
                                                                                              
                                                                                              
    minimum_seats = st.number_input(                                                          
        "Show routes with at least this many available seats",                                
        min_value=0,                                                                          
        step=1                                                                                
    )                                                                                         
                                                                                              
                                                                                              
    if st.button("Filter Routes"):                                                            
        available_routes = []                                                                 
                                                                                              
                                                                                              
        for route in st.session_state.routes_data:                                            
            if route["seats"] >= minimum_seats:                                               
                available_routes.append({                                                     
                    "Route ID": route["route_id"],                                            
                    "Departure": route["departure"],                                          
                    "Destination": route["destination"],                                      
                    "Time": route["time"],                                                    
                    "Fare (PKR)": route["fare"],                                              
                    "Available Seats": route["seats"]                                         
                })                                                                            
                                                                                              
                                                                                              
        if len(available_routes) == 0:                                                        
            st.warning("No routes match this seat requirement.")                              
        else:                                                                                 
            st.table(available_routes)                                                        
                                                                                              
                                                                                              
                                                                                              
                                                                                              
def view_schedule():                                                                          
    st.subheader("Bus Schedule by Departure City")                                            
                                                                                              
                                                                                              
    cities = []                                                                               
    for route in st.session_state.routes_data:                                                
        if route["departure"] not in cities:                                                  
            cities.append(route["departure"])                                                 
                                                                                              
                                                                                              
    for city in cities:                                                                       
        st.markdown("### " + city)                                                            
        city_routes = []                                                                      
                                                                                              
                                                                                              
        for route in st.session_state.routes_data:                                            
            if route["departure"] == city:                                                    
                city_routes.append({                                                          
                    "Route ID": route["route_id"],                                            
                    "Destination": route["destination"],                                      
                    "Departure Time": route["time"],                                          
                    "Fare (PKR)": route["fare"],                                              
                    "Available Seats": route["seats"]                                         
                })                                                                            
                                                                                              
                                                                                              
        st.table(city_routes)                                                                 
                                                                                              
                                                                                              
                                                                                              
                                                                                              
def view_reports():                                                                           
    st.subheader("Booking Reports")                                                           
                                                                                              
                                                                                              
    total_bookings = len(st.session_state.bookings)                                           
    confirmed_bookings = 0                                                                    
    cancelled_bookings = 0                                                                    
    confirmed_seats = 0                                                                       
    confirmed_revenue = 0                                                                     
                                                                                              
                                                                                              
    for booking in st.session_state.bookings:                                                 
        if booking["status"] == "Confirmed":                                                  
            confirmed_bookings += 1                                                           
            confirmed_seats += booking["number_of_seats"]                                     
            confirmed_revenue += booking["total_fare"]                                        
        elif booking["status"] == "Cancelled":                                                
            cancelled_bookings += 1                                                           
                                                                                              
                                                                                              
    fully_booked_routes = 0                                                                   
    for route in st.session_state.routes_data:                                                
        if route["seats"] == 0:                                                               
            fully_booked_routes += 1                                                          
                                                                                              
                                                                                              
    st.write("Total Bookings:", total_bookings)                                               
    st.write("Confirmed Bookings:", confirmed_bookings)                                       
    st.write("Cancelled Bookings:", cancelled_bookings)                                       
    st.write("Seats in Confirmed Bookings:", confirmed_seats)                                 
    st.write("Confirmed Revenue: PKR", confirmed_revenue)                                     
    st.write("Fully Booked Routes:", fully_booked_routes)                                     
                                                                                              
                                                                                              
                                                                                              
                                                                                              
# -------------------- STREAMLIT USER INTERFACE --------------------                          
                                                                                              
                                                                                              
st.title("Smart Bus Ticket Booking System")                                                   
st.write("View routes, search buses, book tickets, and manage reservations.")                 
                                                                                              
                                                                                              
menu = st.sidebar.selectbox(                                                                  
    "Choose an Option",                                                                       
    [                                                                                         
        "View Routes",                                                                        
        "Search Routes",                                                                      
        "Book a Ticket",                                                                      
        "Cancel a Ticket",                                                                    
        "View Bookings",                                                                      
        "Available Seats Filter",                                                             
        "Bus Schedule",                                                                       
        "Reports"                                                                             
    ]                                                                                         
)                                                                                             
                                                                                              
                                                                                              
if menu == "View Routes":                                                                     
    view_routes()                                                                             
elif menu == "Search Routes":                                                                 
    search_routes()                                                                           
elif menu == "Book a Ticket":                                                                 
    book_ticket()                                                                             
elif menu == "Cancel a Ticket":                                                               
    cancel_ticket()                                                                           
elif menu == "View Bookings":                                                                 
    view_bookings()                                                                           
elif menu == "Available Seats Filter":                                                        
    filter_available_routes()                                                                 
elif menu == "Bus Schedule":                                                                  
    view_schedule()                                                                           
elif menu == "Reports":                                                                       
    view_reports()                                                                            
                                                                                              
                                                                                              