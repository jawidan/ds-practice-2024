import React from 'react';
import { useLocation } from 'react-router-dom';

const ConfirmationPage: React.FC = () => {
    const location = useLocation();
    const { orderStatusResponse } = location.state as any;

    // Simplifying the verification status check
    const verificationStatus = orderStatusResponse.verification === 'True' ? 'Success' : 'Failed';
    const isFraudulent = orderStatusResponse.isFraudulent;

    return (
        <div className="container mt-5">
            {/* <h1>Order Confirmation</h1>
            <h2>Order ID: {orderStatusResponse.orderId}</h2> */}
            {/* Update to reflect fraud detection and verification status */}
            <h2>Status: {orderStatusResponse.status}{isFraudulent ? " Fraud Detected" : ""}</h2>
            {verificationStatus === 'Failed' && <h1>Verification Status: {verificationStatus}</h1>}
            {/* Display verification errors if any */}
            {orderStatusResponse.errors && orderStatusResponse.errors.length > 0 && (
                <div>
                    <h3>Verification Errors:</h3>
                    <ul>
                        {orderStatusResponse.errors.map((error: string, index: number) => (
                            <li key={index}>{error}</li>
                        ))}
                    </ul>
                </div>
            )}
            {/* Optionally display fraud reason */}
            {/* {isFraudulent && (
                <div>
                    <h3>Fraud Reason:</h3>
                    <p>{orderStatusResponse.fraudReason}</p>
                </div>
            )} */}
            {/* Suggested books */}
            {orderStatusResponse.suggestedBooks && orderStatusResponse.suggestedBooks.length > 0 && (
                <div>
                    <h3>Suggested Books</h3>
                    <ul>
                        {orderStatusResponse.suggestedBooks.map((book: any, index: number) => (
                            <li key={index}>
                                <h4>{book.title}</h4>
                                <p>Book ID: {book.bookId}<br />
                                Author: {book.author}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default ConfirmationPage;
