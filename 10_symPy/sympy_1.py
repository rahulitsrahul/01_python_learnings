import sympy as sp

# Define symbolic variables
alpha, m, i, j = sp.symbols('alpha m i j')
theta = sp.MatrixSymbol('theta', j, 1)  # Assuming theta is a column vector
X = sp.symbols('X:{}'.format(j))  # Assuming X has j features
y = sp.symbols('y')

# Define the hypothesis function
hypothesis = theta[0] + sum(theta[k + 1] * X[k] for k in range(j))

# Define the cost function
cost = (1 / (2 * m)) * sp.Sum((hypothesis - y)**2, (i, 1, m))

# Compute the partial derivative with respect to theta_j
partial_derivative = sp.diff(cost, theta[j])

# Define the update rule
update_rule = sp.Eq(theta[j], theta[j] - alpha * partial_derivative)

# Print the symbolic expression
print("Update Rule for theta_j:", update_rule)
